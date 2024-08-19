gripe = ["dor de cabeça", "nariz inchado", "dor de garganta", "tosse", "fadiga"]
dengue = ["febre alta", "vômito", "Dor atrás dos olhos", "manchas vermelhas"]
covid = ["perda do paladar", "congestão nasal", "dor de garganta", "dor de cabeça", "dores musculares", "vômito", "diarreia", "calafrios"]
hipertensão= ["dores no peito ", "dor de cabeça", "tonturas", "zumbido no ouvido", "fraqueza", "visão embaçada", "sangramento nasal"]
diabetes= [ "fome frenquente", "sede constante", "vontade de urinar frenquentemente", "perda de peso ",  "fadiga", "mudança de humor", "náusea", "vômito"]
def mal():
    print( gripe )
    print("-" * 40)
    print( dengue )
    print("-" * 40)
    print( covid)
    print("-" * 40)
    print( hipertensão )
    print("-" * 40)
    print( diabetes )
    print ("-" * 40)

mal()

sintomas_usuario = input("Favor digitar os sintomas que está sentindo e que constam no nosso banco de dados: ")
sintomas_usuario = sintomas_usuario.lower()  


if any(sintoma in sintomas_usuario for sintoma in gripe):
    print("Você está com gripe.")
elif any(sintoma in sintomas_usuario for sintoma in covid):
    print("Você está com covid.")
elif any(sintoma in sintomas_usuario for sintoma in dengue):
    print("Você está com dengue.")
elif any(sintoma in sintomas_usuario for sintoma in hipertensão):
    print("Você está com hipertensão")
elif any (sintoma in sintoma_usuario for sintoma in diabetes):
    print("você está com diabetes")
else:
    print("Não foi possível determinar a doença com base nos sintomas fornecidos.")

dias_sintomas = int(input("Digite há quantos dias você está sentindo esses sintomas: "))


if dias_sintomas >= 1 and dias_sintomas < 4:
    print("Procure ajuda médica assim que possível.")
elif dias_sintomas >= 5:
    print("Procure um médico nas próximas horas.")
else:
    print("Vá ao médico imediatamente.")