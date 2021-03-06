#===============================================================================
#conexion_Telnet: Habilitar BGP
#Parametros:
# objeto_Telnet(Telnet):  objeto  Telnet
# Sistema_Autonomo(str):  usuario del dispositivo
#
#-------------------------------------------------------------------------------

def sesion_BGP(objeto_Telnet,Sistema_Autonomo):
    
    ingreso_Router=str("router bgp "+Sistema_Autonomo+"\n")
    print(ingreso_Router)
    objeto_Telnet.write(ingreso_Router.encode('ascii'))

#===============================================================================
#es_Local: Permite comparar un String para saber si es estamos configurando
#           el router local o el remoto
#Parametros:
# Local_OR_Remoto  (str):  variable a comparar 
#Retorna:
# True or False(boolean): resultado de la comparación 
#-------------------------------------------------------------------------------

def es_Local(Local_OR_Remoto):
    if Local_OR_Remoto.lower().strip()=="local":
        return True
    else:
        return False

#===============================================================================
#configurar_Network: Anuncia las redes que son ingresadas como parametro de entrada
#Parametros:
# objeto_Telnet(Telnet):  objeto  Telnet
# lista_Networks(lista):  contiene una lista de strings que corresponden al
#                           grupo de networks a configurar en el router.
#
#-------------------------------------------------------------------------------

def configurar_Network(objeto_Telnet,lista_Networks):
    for network in lista_Networks:
        if(network.strip()=="0.0.0.0"):
            red=str("network "+ network+"\n")
            objeto_Telnet.write(red.encode('ascii'))
        else:
            red=network.split('-')
            red_Y_mask=str("network "+red[0]+" mask "+red[1]+"\n")
            print (red_Y_mask)
            objeto_Telnet.write(red_Y_mask.encode('ascii'))
    

#===============================================================================
#config_Vecino: Configura el router vecino con su AS
#Parametros:
# objeto_Telnet(Telnet):  objeto  Telnet
# ip_Vecino (str):  Dirección IP de la interfaz vecina
# AS_Local  (str): Sistema Autónomo del Router Local
# AS_Remoto (str): Sistema Autónomo del Router Remoto
# lista_Networks(lista):  contiene una lista de strings que corresponden al
#                           grupo de networks a configurar en el router.
# var_Local (str):  variable indicador, separa la configuración que recibe el
#                   Router local y la que recibe el remoto.
#-------------------------------------------------------------------------------


def config_Vecino(objeto_Telnet,ip_local,ip_Vecino,AS_Local,AS_Remoto,lista_NetworksL,lista_NetworksR,usuario,contraseña):
    sesion_BGP(objeto_Telnet,AS_Local)
    objeto_Telnet.write("\n".encode('ascii'))
    vecino=str("neighbor " +ip_Vecino+ " remote-as "+AS_Remoto+"\n")
    objeto_Telnet.write(vecino.encode('ascii'))
    configurar_Network(objeto_Telnet,lista_NetworksL)

    objeto_Telnet.write("end\n".encode('ascii'))
    objeto_Telnet.write("wr\n".encode('ascii'))
    objeto_Telnet.write("\n".encode('ascii'))
        
    objeto_Telnet.write(("telnet {}\n").format(ip_Vecino).encode('ascii'))
    objeto_Telnet.write(("{}\n").format(usuario).encode('ascii'))
    objeto_Telnet.write(("{}\n").format(contraseña).encode('ascii'))

    
    objeto_Telnet.write("enable \n".encode('ascii'))
    objeto_Telnet.write("config t\n".encode('ascii'))
        
    objeto_Telnet.write("ip route 0.0.0.0 0.0.0.0 lo0 name to_core_isp \n".encode('ascii'))
    sesion_BGP(objeto_Telnet,AS_Remoto)
    vecino_Local=str("neighbor " +ip_local+ " remote-as "+AS_Local+"\n")
    objeto_Telnet.write(vecino_Local.encode('ascii'))
    configurar_Network(objeto_Telnet,lista_NetworksR)
    print("Se configuró BGP con éxito")



