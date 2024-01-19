import PyPtt
import requests
import time
import re
import random

TELEGRAM_ID_BOCHENZ = '6713518495'

def pttLogin():

    max_retry = 5

    ptt_bot = None
    for retry_time in range(max_retry):
        try:
            ptt_bot = PyPtt.API()

            ptt_bot.login('', '', kick_other_session=False if retry_time == 0 else True)
            break
        except PyPtt.exceptions.LoginError:
            ptt_bot = None
            print('登入失敗')
            time.sleep(3)
        except PyPtt.exceptions.LoginTooOften:
            ptt_bot = None
            print('請稍後再試')
            time.sleep(60)
        except PyPtt.exceptions.WrongIDorPassword:
            print('帳號密碼錯誤')
            raise
        except Exception as e:
            print('其他錯誤:', e)
            break

    return ptt_bot

def send_msg(msg:str, token:str, chatID:str):

    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chatID}&text={msg}'
    requests.get(url)

def main() -> None:

    re_str = ['(\\[)*賣.*([34]0[789]0).*','(\\[)*賣.*(螢幕|屏(幕)*|xv27|mpg321ur|pg32u).*']

    ptt_bot = pttLogin()

    first_time_excute = True
    url_list = []
    last_newest_index = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Hardwaresale')

    first_time_excute_life = True
    url_list_life = []
    last_newest_index_life = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Lifeismoney')

    first_time_excute_steam = True
    url_list_steam = []
    last_newest_index_steam = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Steam')

    try:
        while True:

            try:
                newest_index = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Hardwaresale')
                newest_index_life = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Lifeismoney')
                newest_index_steam = ptt_bot.get_newest_index(PyPtt.NewIndex.BOARD, 'Steam')

            except PyPtt.exceptions.ConnectionClosed:
                ptt_bot = pttLogin()
                continue
            except Exception as e:
                print('其他錯誤:', e)
                break

            if newest_index == last_newest_index and not first_time_excute:
                url_list = []
                print(".", end="")
            else:
            
                if not first_time_excute:
                    last_newest_index += 1

                first_time_excute = False
                

                #find new post

                for i in range(last_newest_index, newest_index+1):
                    post_info = ptt_bot.get_post('Hardwaresale', index=i)

                    print(post_info['title'])

                    for reStr in re_str:
                        if post_info['title'] and re.match(reStr, post_info['title'], re.IGNORECASE):
                            url_list.append([post_info['title'], post_info['url']])
                            break

                #print(url_list)
                
                if len(url_list) > 0:
                    str_tmp = ""
                    for item in url_list:
                        str_tmp += f'{item[0]}\n{item[1]}\n'
                    send_msg(str_tmp, "", "5512217147")

                last_newest_index = newest_index





            if newest_index_life == last_newest_index_life and not first_time_excute_life:
                url_list_life = []
                print(".", end="")
            else:
            
                if not first_time_excute_life:
                    last_newest_index_life += 1

                first_time_excute_life = False
                

                #find new post

                for i in range(last_newest_index_life, newest_index_life+1):
                    post_info = ptt_bot.get_post('Lifeismoney', index=i)

                    print(post_info['title'])

                    if post_info['title'] and re.match('.*情報.*', post_info['title'], re.IGNORECASE):
                        url_list_life.append([post_info['title'], post_info['url']])

                #print(url_list)
                
                if len(url_list_life) > 0:
                    str_tmp = ""
                    for item in url_list_life:
                        str_tmp += f'{item[0]}\n{item[1]}\n'
                    send_msg(str_tmp, "", "5512217147")
                    send_msg(str_tmp, "", TELEGRAM_ID_BOCHENZ)

                last_newest_index_life = newest_index_life




            if newest_index_steam == last_newest_index_steam and not first_time_excute_steam:
                url_list_steam = []
                print(".", end="")
            else:
            
                if not first_time_excute_steam:
                    last_newest_index_steam += 1

                first_time_excute_steam = False
                

                #find new post

                for i in range(last_newest_index_steam, newest_index_steam+1):
                    post_info = ptt_bot.get_post('Steam', index=i)

                    print(post_info['title'])

                    if post_info['title'] and re.match('.*限免.*', post_info['title'], re.IGNORECASE):
                        url_list_steam.append([post_info['title'], post_info['url']])

                #print(url_list)
                
                if len(url_list_steam) > 0:
                    str_tmp = ""
                    for item in url_list_steam:
                        str_tmp += f'{item[0]}\n{item[1]}\n'
                    send_msg(str_tmp, "", "5512217147")
                    send_msg(str_tmp, "", TELEGRAM_ID_BOCHENZ)

                last_newest_index_steam = newest_index_steam
                

            
            
            time.sleep(2+random.randint(1,20)/10)
    finally:
        ptt_bot.logout()


if __name__ == "__main__":
    main()
