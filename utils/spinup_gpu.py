import boto3
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Параметры EC2 для запуска инстанса
INSTANCE_TYPE = 'p3.2xlarge'  # Указываем тип инстанса с GPU (например, p3.2xlarge)
AMI_ID = 'ami-xxxxxxxx'       # Замените на свой ID AMI с предустановленным окружением
KEY_NAME = 'your-key-name'    # Имя вашего ключа для SSH доступа

# Инициализация клиента EC2
ec2 = boto3.client('ec2', region_name='us-west-2')  # Замените регион на нужный

def start_gpu_instance():
    """
     Функция для запуска EC2 инстанса с GPU.
    """
    try:
        # Запуск EC2 инстанса
        logging.info("Запуск EC2 инстанса с GPU...")
        response = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            KeyName=KEY_NAME,
            SecurityGroups=['your-security-group'],  # Замените на ваш Security Group
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'GPU Instance'}
                    ]
                }
            ]
        )
        instance_id = response['Instances'][0]['InstanceId']
        logging.info(f"Инстанс с ID {instance_id} был успешно запущен.")

        # Ожидаем, пока инстанс не станет доступным
        ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        logging.info(f"Инстанс {instance_id} теперь в статусе running.")

        # Возвращаем ID инстанса
        return instance_id

    except Exception as e:
        logging.error(f"Ошибка при запуске инстанса: {e}")
        raise

if __name__ == "__main__":
    start_gpu_instance()
