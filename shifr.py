ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789.,;:!?-() "

def encrypt_string(original_string,key):
    result_string="" 
    for item in original_string:
        index=ALPHABET.find(item)
        if index == -1:
            result_string += item
        else:
            new_index = (index + key) % len(ALPHABET)
            result_string += ALPHABET[new_index]

    return result_string


def decrypt_string(original_string,key):
    result_string="" 
    for item in original_string:
        index=ALPHABET.find(item)
        if index == -1:
            result_string += item
        else:
            new_index = (index + key) % len(ALPHABET)
            result_string += ALPHABET[new_index]

    return result_string








operationg_mode=int(input("введите режим работы 1-шифрование,2-деифрование"))
original_string=input( "введите обычную строку ")
key=input( "введите ключ ")

result_string="" 

if operationg_mode ==1:
    result_string=encrypt_string(original_string,key)
elif operationg_mode==2:
    result_string=decrypt_string(original_string,key)




print(f"результат= {result_string}")