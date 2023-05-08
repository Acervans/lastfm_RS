#include <stdio.h>
#include <stdlib.h>
#include <redes2/irc.h>

#include <redes2/ircinternals.h>

/** 
 * @defgroup IRCMessageErrorUserConnect Mensajes relacionados con la conexión de usuarios
 * @ingroup IRCMessageError
 *
 */
 
/** 
 * @defgroup IRCMessageReplyUserConnect Mensajes relacionados con la conexión de usuarios
 * @ingroup IRCMessageReply
 *
 */

/** 
 * @addtogroup IRCMessageErrorUserConnect
 * Funciones para la creación de respuestas de error IRC. Estas respuestas las dan tanto servidores como clientes
 * cuando tienen que comunicar a la contraparte de algún error. Grupo de mensajes de error relacionado con 
 * la conexión de usuarios.
 *
 * <hr>
 */

/** 
 * @addtogroup IRCMessageReplyUserConnect
 * Funciones para la creación de respuestas IRC. Estas funciones permiten construir las respuestas normales
 * a los mensajes de la contraparte. Grupo de mensajes de respuesta relacionado con la conexión de usuarios.
 *
 * <hr>
 */



/**
 * @ingroup IRCMessageErrorUserConnect
 *
 * @page IRCMsg_ErrAlreadyRegistred IRCMsg_ErrAlreadyRegistred
 *
 * @brief Parse de ERR_ALREADYREGISTRED.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_ErrAlreadyRegistred (char **command, char *prefix, char * nick)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 * 
 * \b ERR_ALREADYREGISTRED \par
 * 
 * Returned by the server to any link which tries to
 * change part of the registered details (such as
 * password or user details from second USER message).
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_ErrAlreadyRegistred(char **command, char *prefix, char *nick)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	__CPM__(command,prefix,COM_ERR_ALREADYREGISTRED,nick,"Unauthorized command (already registered)");
	return IRC_OK;
}

/**
 * @ingroup IRCMessageErrorUserConnect
 *
 * @page IRCMsg_ErrErroneusNickName IRCMsg_ErrErroneusNickName
 *
 * @brief Parse de ERR_ERRONEUSNICKNAME.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_ErrErroneusNickName (char **command, char *prefix, char * nick, char *erroneusnick)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCMsg tiene en el primer parámetro
 * es un apuntador la string a que se va a crear. Las funciones le hacen sitio internamente
 * y por tanto es responsabilidad del programador liberarlo. Los siguientes parámetros son las
 * strings o enteros que se van a utilizar para construir los mensanjes. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales.  \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa. 
 * \par
 *
 * \b ERR_ERRONEUSNICKNAME \par
 * 
 * Returned after receiving a NICK message which contains
 * characters which do not fall in the defined set.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 * @retval IRCERR_NOERRONEUSNICK: No se ha introducido el nickerróneo.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_ErrErroneusNickName(char **command, char *prefix, char *nick, char *erroneusnick)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	if(erroneusnick == NULL) return IRCERR_NOERRONEUSNICK;
	__CPPM__(command,prefix,COM_ERR_ERRONEUSNICKNAME,nick,erroneusnick,"Erroneous nickname");
	return IRC_OK;
}          
  
/**
 * @ingroup IRCMessageErrorUserConnect
 *
 * @page IRCMsg_ErrNickCollision IRCMsg_ErrNickCollision
 *
 * @brief Parse de ERR_NICKCOLLISION.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_ErrNickCollision (char **command, char *prefix, char * nick, char *nick2, char *user, char *host)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b ERR_NICKCOLLISION \par
 * 
 * Returned by a server to a client when it detects a
 * nickname collision (registered of a NICK that
 * already exists by another server).
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 * @retval IRCERR_NOUSER No se ha introducido un user.
 * @retval IRCERR_NOHOST No se ha introducido un host.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_ErrNickCollision(char **command, char *prefix, char *nick, char *nick2, char *user, char *host)
{
	char aux[64];

	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	if(nick2 == NULL) return IRCERR_NONICK;
	if(user == NULL) return IRCERR_NOUSER;
	if(host == NULL) return IRCERR_NOHOST;
	sprintf(aux,"Nickname collision KILL from %s@%s",user,host);
	__CPPM__(command,prefix,COM_ERR_NICKCOLLISION,nick,nick2,aux);
	return IRC_OK;
}

/**
 * @ingroup IRCMessageErrorUserConnect
 *
 * @page IRCMsg_ErrNickNameInUse IRCMsg_ErrNickNameInUse
 *
 * @brief Parse de ERR_NICKNAMEINUSE.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_ErrNickNameInUse (char **command, char *prefix, char * nick, char *erroneusnick)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b ERR_NICKNAMEINUSE \par
 * 
 * Returned when a NICK message is processed that results
 * in an attempt to change to a currently existing
 * nickname.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 * @retval IRCERR_NOERRONEUSNICK: No se ha introducido el nick erróneo.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_ErrNickNameInUse(char **command, char *prefix, char *nick, char *erroneusnick)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	if(erroneusnick == NULL) return IRCERR_NOERRONEUSNICK;
	__CPPM__(command,prefix,COM_ERR_NICKNAMEINUSE,nick,erroneusnick,"Nickname is already in use");
	return IRC_OK;
}
                

/**
 * @ingroup IRCMessageErrorUserConnect
 *
 * @page IRCMsg_ErrNoOperHost IRCMsg_ErrNoOperHost
 *
 * @brief Parse de ERR_NOOPERHOST.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_ErrNoOperHost (char **command, char *prefix, char * nick)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b ERR_NOOPERHOST \par
 * 
 * If a client sends an OPER message and the server has
 * not been configured to allow connections from the
 * client's host as an operator, this error MUST be
 * returned.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_ErrNoOperHost(char **command, char *prefix, char *nick)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	__CPM__(command,prefix,COM_ERR_NOOPERHOST,nick,"No O-lines for your host");
	return IRC_OK;
}

/**
 * @ingroup IRCMessageErrorUserConnect
 *
 * @page IRCMsg_ErrUModeUnknownFlag IRCMsg_ErrUModeUnknownFlag
 *
 * @brief Parse de PASS.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_ErrUModeUnknownFlag (char **command, char *prefix, char * nick)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b ERR_UMODEUNKNOWNFLAG \par
 * 
 * Returned by the server to indicate that a MODE
 * message was sent with a nickname parameter and that
 * the a mode flag sent was not recognized.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_ErrUModeUnknownFlag(char **command, char *prefix, char *nick)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	__CPM__(command,prefix,COM_ERR_UMODEUNKNOWNFLAG,nick,"Unknown MODE flag");
	return IRC_OK;
}

/**
 * @ingroup IRCMessageErrorUserConnect
 *
 * @page IRCMsg_ErrUsersDontMatch IRCMsg_ErrUsersDontMatch
 *
 * @brief Parse de ERR_USERSDONTMATCH.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_ErrUsersDontMatch (char **command, char *prefix, char * password)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b ERR_USERSDONTMATCH \par
 * 
 * Error sent to any user trying to view or change the
 * user mode for a user other than themselves.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_ErrUsersDontMatch(char **command, char *prefix, char *nick)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	__CPM__(command,prefix,COM_ERR_USERSDONTMATCH,nick,"Cannot change mode for other users");
	return IRC_OK;
}



/**
 * @ingroup IRCMessageReplyUserConnect
 *
 * @page IRCMsg_RplMyInfo IRCMsg_RplMyInfo
 *
 * @brief Parse de RPL_MYINFO.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_RplMyInfo(char **command, char *prefix, char *nick, char *servername, char *version, char *availableusermodes, char *availablechannelmodes)
 * @endcode
 * 
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b RPL_MYINFO \par
 * 
 * The server sends Replies 001 to 004 to a user upon
 * successful registration.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 * @retval IRCERR_NOSERVERNAME No se ha introducido el un nombre de servidor.
 * @retval IRCERR_NOVERSION: No se ha introducido la versión.
 * @retval IRCERR_NOAVAILABLEUSERMODES: No se han introducido los modos de usuario utilizables.
 * @retval IRCERR_NOAVAILABLECHANNEL: No se han introducido el los mosdos de canal utilizables.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/
   
long IRCMsg_RplMyInfo(char **command, char *prefix, char *nick, char *servername, char *version, char *availableusermodes, char *availablechannelmodes)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	if(servername == NULL) return IRCERR_NOSERVERNAME;
	if(version == NULL) return IRCERR_NOVERSION;
	if(availableusermodes == NULL) return IRCERR_NOAVAILABLEUSERMODES;
	if(availablechannelmodes == NULL) return IRCERR_NOAVAILABLECHANNEL;
	__CPPPPP__(command,prefix,COM_RPL_MYINFO,nick,servername,version,availableusermodes,availableusermodes);
	return IRC_OK;
}
  
/**
 * @ingroup IRCMessageReplyUserConnect
 *
 * @page IRCMsg_RplUModeIs IRCMsg_RplUModeIs
 *
 * @brief Parse de RPL_UMODEIS.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_RplUModeIs (char **command, char *prefix, char * nick, char *usermodestring)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b RPL_UMODEIS \par
 * 
 * To answer a query about a client's own mode,
 * RPL_UMODEIS is sent back.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 * @retval IRCERR_NOUSERMODESTRING: No se ha introducido una string de modo.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_RplUModeIs(char **command, char *prefix, char *nick, char *usermodestring)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	if(usermodestring == NULL) return IRCERR_NOUSERMODESTRING;
	__CPP__(command,prefix,COM_RPL_UMODEIS,nick,usermodestring);
	return IRC_OK;
}


/**
 * @ingroup IRCMessageReplyUserConnect
 *
 * @page IRCMsg_RplYoureOper IRCMsg_RplYoureOper
 *
 * @brief Parse de RPL_OPER.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_RplYoureOper (char **command, char *prefix, char * nick)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b RPL_OPER \par
 * 
 * Is sent back to a client which has
 * just successfully issued an OPER message and gained
 * operator status.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_RplYoureOper(char **command, char *prefix, char *nick)
{
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	__CPM__(command,prefix,COM_RPL_YOUREOPER,nick,"You are now an IRC operator");
	return IRC_OK;
}

/**
 * @ingroup IRCMessageReplyUserConnect
 *
 * @page IRCMsg_RplYoureService IRCMsg_RplYoureService
 *
 * @brief Parse de RPL_YOURESERVICE.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_RplYoureService (char **command, char *prefix, char * nick, char *servicename)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b RPL_YOURESERVICE \par
 * 
 * Sent by the server to a service upon successful
 * registration.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 * @retval IRCERR_NOSERVICENAME: no se ha proporcionado el nombre de un servicio.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_RplYoureService(char **command, char *prefix, char *nick, char *servicename)
{
	char aux[128];
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	if(servicename == NULL) return IRCERR_NOSERVICENAME;
	sprintf(aux,"You are service %s",servicename);
	__CPM__(command,prefix,COM_RPL_YOURESERVICE,nick,aux);
	return IRC_OK;
}


/**
 * @ingroup IRCMessageReplyUserConnect
 *
 * @page IRCMsg_RplYourHost IRCMsg_RplYourHost
 *
 * @brief Parse de RPL_YOURHOST.
 *
 * @synopsis
 * @code
 *	#include <redes2/irc.h>
 *
 *	long IRCMsg_RplYourHost (char **command, char *prefix, char * nick, char *servername, char *versionname)
 * @endcode
 *
 * @description
 * Como todos los comandos de la familia IRCParse tiene en el primer parámetro
 * la string a parsear y en los siguientes parámetros hay apuntadores a los 
 * strings o enteros que van a ser extraidos de la string a parsear. Los 
 * strings a NULL o los enteros a 0 son válidos e indican que dichos parámetros
 * no están presentes en la string parseada cuando dichos valores son opcionales. \par
 *
 * Las funciones de creación de mensajes reciben un apuntador a una string donde se almacena el 
 * comando. La función reserva memoria internamente para esta string y debe ser liberada por el
 * programador cuando lo considere necesario. \par
 * 
 * Este comando pertenece a los RFCs de IRC (RFC-1459, RFC-2810, RFC-2811, 
 * RFC-2812, RFC-2813 y RFC-2814), por tanto es necesario leérselos para
 * entender su funcionamiento. Se copia la descripción de la parte del RFC
 * relativa al comando pero es necesario entenderlo en el contexto del RFC
 * con lo que se recomienda su lectura completa.  \par
 *
 * \b RPL_YOURHOST \par
 * 
 * The server sends Replies 001 to 004 to a user upon
 * successful registration.
 *
 * @retval IRC_OK Sin error
 * @retval IRCERR_NONICK No se ha introducido un nick.
 * @retval IRCERR_NOSERVERNAME no se ha proporcionado el nombre de un servidor.
 *
 * @author
 * Eloy Anguiano (eloy.anguiano@uam.es)
 *
 *<hr>
*/

long IRCMsg_RplYourHost(char **command, char *prefix, char *nick, char *servername, char *versionname)
{
	char aux[128];
	*command=0;
	if(nick == NULL) return IRCERR_NONICK;
	if(servername == NULL) return IRCERR_NOSERVERNAME;
	sprintf(aux,"Your host is %s, running version %s",servername,versionname);
	__CPM__(command,prefix,COM_RPL_YOURHOST,nick,aux);
	return IRC_OK;
}



