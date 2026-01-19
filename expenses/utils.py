from datetime import date
from dateutil.relativedelta import relativedelta 
from .models import Transaction, RecurringTransaction

def generate_recurring_transactions():
    """Lógica para criar transações baseadas nas recorrências ativas"""
    today = date.today()
    recurrences = RecurringTransaction.objects.filter(is_active=True)
    count = 0

    for rec in recurrences:
        # Se nunca foi gerada, a próxima data é a start_date
        # Se já foi gerada, a próxima é last_generated + 1 mês (ou semana)
        next_date = rec.last_generated_date or rec.start_date
        
        # Se a próxima data já passou ou é hoje, criamos a transação
        while next_date <= today:
            # Evita criar duplicatas se a transação já existir para essa data
            exists = Transaction.objects.filter(
                user=rec.user, 
                description=rec.description, 
                date=next_date
            ).exists()

            if not exists:
                Transaction.objects.create(
                    user=rec.user,
                    description=rec.description,
                    amount=rec.amount,
                    type=rec.type,
                    category=rec.category,
                    payment_method=rec.payment_method,
                    date=next_date,
                    status='PENDING' # Recorrência nasce como pendente
                )
                count += 1

            # Avança para a próxima ocorrência baseada na frequência
            if rec.frequency == 'WEEKLY':
                next_date += relativedelta(weeks=1)
            elif rec.frequency == 'MONTHLY':
                next_date += relativedelta(months=1)
            elif rec.frequency == 'YEARLY':
                next_date += relativedelta(years=1)

            # Atualiza a recorrência
            rec.last_generated_date = next_date
            rec.save()
            
            # Se tiver data de término e passamos dela, desativa
            if rec.end_date and next_date > rec.end_date:
                rec.is_active = False
                rec.save()
                break
    return count