https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#databases:

Create Databse

MYSQL


Free Tier

enter username
enter password

for now Public access is yes, after that is working configure the security group


Once you have 

If you have a ec2 instance launch then you can launch a rds instance inside the same security group and then add a inbound rule to use type MYSQL/Auora with the source being the same security group as the ec2 insatnce


if you place a rds instance in the same ec2 security group and open 
