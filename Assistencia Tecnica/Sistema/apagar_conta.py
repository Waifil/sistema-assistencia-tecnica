import database

resultado = database.apagar_tudo()

if resultado:
    print("Contas apagadas com sucesso!")
else:
    print("Não foi possível apagar as contas.")