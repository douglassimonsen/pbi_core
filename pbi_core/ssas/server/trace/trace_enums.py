# C:\Program Files\Microsoft SQL Server\MSAS16.MSSQLSERVER\OLAP\bin\Resources\1033\tracedefinition.xml
# ruff: noqa: E501
from enum import IntEnum


class TraceEvents(IntEnum):
    COMMAND_BEGIN = 15  # Command begin.
    COMMAND_END = 16  # Command end.
    DISCOVER_BEGIN = 36  # Start of Discover Request.
    DISCOVER_END = 38  # End of Discover Request.
    SERVER_STATE_DISCOVER_BEGIN = 33  # Start of Server State Discover.
    SERVER_STATE_DISCOVER_DATA = 34  # Contents of the Server State Discover Response.
    SERVER_STATE_DISCOVER_END = 35  # End of Server State Discover.
    ERROR = 17  # Server error.
    FILE_LOAD_BEGIN = 90  # File Load Begin.
    FILE_LOAD_END = 91  # File Load End.
    FILE_SAVE_BEGIN = 92  # File Save Begin.
    FILE_SAVE_END = 93  # File Save End
    PAGEOUT_BEGIN = 94  # PageOut Begin.
    PAGEOUT_END = 95  # PageOut End
    PAGEIN_BEGIN = 96  # PageIn Begin.
    PAGEIN_END = 97  # PageIn End
    JOB_GRAPH = 134  # Collection of Job Graph related events.
    DEADLOCK = 50  # Metadata locks deadlock.
    LOCK_TIMEOUT = 51  # Metadata lock timeout.
    LOCK_ACQUIRED = 52  # Lock Acquired
    LOCK_RELEASED = 53  # Lock Released
    LOCK_WAITING = 54  # Lock Waiting
    NOTIFICATION = 39  # Notification event.
    USER_DEFINED = 40  # User defined Event.
    PROGRESS_REPORT_BEGIN = 5  # Progress report begins.
    PROGRESS_REPORT_END = 6  # Progress report end.
    PROGRESS_REPORT_CURRENT = 7  # Progress report current.
    PROGRESS_REPORT_ERROR = 8  # Progress report error.
    QUERY_BEGIN = 9  # Query begins.
    QUERY_END = 10  # Query end.
    QUERY_CUBE_BEGIN = 70  # Query cube begin.
    QUERY_CUBE_END = 71  # Query cube end.
    CALCULATE_NON_EMPTY_BEGIN = 72  # Calculate non empty begin.
    CALCULATE_NON_EMPTY_CURRENT = 73  # Calculate non empty current.
    CALCULATE_NON_EMPTY_END = 74  # Calculate non empty end.
    SERIALIZE_RESULTS_BEGIN = 75  # Serialize results begin.
    SERIALIZE_RESULTS_CURRENT = 76  # Serialize results current.
    SERIALIZE_RESULTS_END = 77  # Serialize results end.
    EXECUTE_MDX_SCRIPT_BEGIN = 78  # Execute MDX script begin.
    EXECUTE_MDX_SCRIPT_CURRENT = 79  # Execute MDX script current. Deprecated.
    EXECUTE_MDX_SCRIPT_END = 80  # Execute MDX script end.
    QUERY_DIMENSION = 81  # Query dimension.
    QUERY_SUBCUBE = 11  # Query subcube, for Usage Based Optimization.
    QUERY_SUBCUBE_VERBOSE = 12  # Query subcube with detailed information. This event may have a negative impact on performance when turned on.
    GET_DATA_FROM_AGGREGATION = 60  # Answer query by getting data from aggregation. This event may have a negative impact on performance when turned on.
    GET_DATA_FROM_CACHE = 61  # Answer query by getting data from one of the caches. This event may have a negative impact on performance when turned on.
    VERTIPAQ_SE_QUERY_BEGIN = 82  # VertiPaq SE query
    VERTIPAQ_SE_QUERY_END = 83  # VertiPaq SE query
    RESOURCE_USAGE = 84  # Reports reads, writes, cpu usage after end of commands and queries.
    VERTIPAQ_SE_QUERY_CACHE_MATCH = 85  # VertiPaq SE query cache use
    DIRECT_QUERY_BEGIN = 98  # Direct Query Begin.
    DIRECT_QUERY_END = 99  # Direct Query End.
    AUDIT_LOGIN = 1  # Collects all new connection events since the trace was started, such as when a client requests a connection to a server running an instance of SQL Server.
    AUDIT_LOGOUT = 2  # Collects all new disconnect events since the trace was started, such as when a client issues a disconnect command.
    AUDIT_SERVER_STARTS_AND_STOPS = 4  # Records service shut down, start, and pause activities.
    AUDIT_OBJECT_PERMISSION_EVENT = 18  # Records object permission changes.
    AUDIT_ADMIN_OPERATIONS_EVENT = 19  # Records server backup/restore/synchronize/attach/detach/imageload/imagesave.
    EXISTING_CONNECTION = 41  # Existing user connection.
    EXISTING_SESSION = 42  # Existing session.
    SESSION_INITIALIZE = 43  # Session Initialize.

    def get_columns(self) -> IntEnum:
        return event_column_mapping[self]


class DiscoverBeginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class.  The following are valid Sub Class Id/Sub Class Name value pairs: 0: DBSCHEMA_CATALOGS 1: DBSCHEMA_TABLES 2: DBSCHEMA_COLUMNS 3: DBSCHEMA_PROVIDER_TYPES 4: MDSCHEMA_CUBES 5: MDSCHEMA_DIMENSIONS 6: MDSCHEMA_HIERARCHIES 7: MDSCHEMA_LEVELS 8: MDSCHEMA_MEASURES 9: MDSCHEMA_PROPERTIES 10: MDSCHEMA_MEMBERS 11: MDSCHEMA_FUNCTIONS 12: MDSCHEMA_ACTIONS 13: MDSCHEMA_SETS 14: DISCOVER_INSTANCES 15: MDSCHEMA_KPIS 16: MDSCHEMA_MEASUREGROUPS 17: MDSCHEMA_COMMANDS 18: DMSCHEMA_MINING_SERVICES 19: DMSCHEMA_MINING_SERVICE_PARAMETERS 20: DMSCHEMA_MINING_FUNCTIONS 21: DMSCHEMA_MINING_MODEL_CONTENT 22: DMSCHEMA_MINING_MODEL_XML 23: DMSCHEMA_MINING_MODELS 24: DMSCHEMA_MINING_COLUMNS 25: DISCOVER_DATASOURCES 26: DISCOVER_PROPERTIES 27: DISCOVER_SCHEMA_ROWSETS 28: DISCOVER_ENUMERATORS 29: DISCOVER_KEYWORDS 30: DISCOVER_LITERALS 31: DISCOVER_XML_METADATA 32: DISCOVER_TRACES 33: DISCOVER_TRACE_DEFINITION_PROVIDERINFO 34: DISCOVER_TRACE_COLUMNS 35: DISCOVER_TRACE_EVENT_CATEGORIES 36: DMSCHEMA_MINING_STRUCTURES 37: DMSCHEMA_MINING_STRUCTURE_COLUMNS 38: DISCOVER_MASTER_KEY 39: MDSCHEMA_INPUT_DATASOURCES 40: DISCOVER_LOCATIONS 41: DISCOVER_PARTITION_DIMENSION_STAT 42: DISCOVER_PARTITION_STAT 43: DISCOVER_DIMENSION_STAT 44: MDSCHEMA_MEASUREGROUP_DIMENSIONS 45: DISCOVER_XEVENT_PACKAGES 46: DISCOVER_XEVENT_OBJECTS 47: DISCOVER_XEVENT_OBJECT_COLUMNS 48: DISCOVER_XEVENT_SESSION_TARGETS 49: DISCOVER_XEVENT_SESSIONS 50: DISCOVER_STORAGE_TABLES 51: DISCOVER_STORAGE_TABLE_COLUMNS 52: DISCOVER_STORAGE_TABLE_COLUMN_SEGMENTS 53: DISCOVER_CALC_DEPENDENCY 54: DISCOVER_CSDL_METADATA 55: DISCOVER_RESOURCE_POOLS 56: TMSCHEMA_MODEL 57: TMSCHEMA_DATA_SOURCES 58: TMSCHEMA_TABLES 59: TMSCHEMA_COLUMNS 60: TMSCHEMA_ATTRIBUTE_HIERARCHIES 61: TMSCHEMA_PARTITIONS 62: TMSCHEMA_RELATIONSHIPS 63: TMSCHEMA_MEASURES 64: TMSCHEMA_HIERARCHIES 65: TMSCHEMA_LEVELS 67: TMSCHEMA_TABLE_STORAGES 68: TMSCHEMA_COLUMN_STORAGES 69: TMSCHEMA_PARTITION_STORAGES 70: TMSCHEMA_SEGMENT_MAP_STORAGES 71: TMSCHEMA_DICTIONARY_STORAGES 72: TMSCHEMA_COLUMN_PARTITION_STORAGES 73: TMSCHEMA_RELATIONSHIP_STORAGES 74: TMSCHEMA_RELATIONSHIP_INDEX_STORAGES 75: TMSCHEMA_ATTRIBUTE_HIERARCHY_STORAGES 76: TMSCHEMA_HIERARCHY_STORAGES 77: DISCOVER_RING_BUFFERS 78: TMSCHEMA_KPIS 79: TMSCHEMA_STORAGE_FOLDERS 80: TMSCHEMA_STORAGE_FILES 81: TMSCHEMA_SEGMENT_STORAGES 82: TMSCHEMA_CULTURES 83: TMSCHEMA_OBJECT_TRANSLATIONS 84: TMSCHEMA_LINGUISTIC_METADATA 85: TMSCHEMA_ANNOTATIONS 86: TMSCHEMA_PERSPECTIVES 87: TMSCHEMA_PERSPECTIVE_TABLES 88: TMSCHEMA_PERSPECTIVE_COLUMNS 89: TMSCHEMA_PERSPECTIVE_HIERARCHIES 90: TMSCHEMA_PERSPECTIVE_MEASURES  95: TMSCHEMA_SETS 96: TMSCHEMA_PERSPECTIVE_SETS 97: TMSCHEMA_EXTENDED_PROPERTIES 98: TMSCHEMA_EXPRESSIONS 99: TMSCHEMA_COLUMN_PERMISSIONS 100: TMSCHEMA_DETAIL_ROWS_DEFINITIONS 101: TMSCHEMA_RELATED_COLUMN_DETAILS 102: TMSCHEMA_GROUP_BY_COLUMNS 103: TMSCHEMA_CALCULATION_GROUPS 104: TMSCHEMA_CALCULATION_ITEMS 105: TMSCHEMA_ALTERNATE_OF_DEFINITIONS 106: TMSCHEMA_REFRESH_POLICIES 107: DISCOVER_POWERBI_DATASOURCES 108: TMSCHEMA_FORMAT_STRING_DEFINITIONS 109: DISCOVER_M_EXPRESSIONS 110: TMSCHEMA_POWERBI_ROLES 111: TMSCHEMA_QUERY_GROUPS 112: DISCOVER_DB_MEM_STATS 113: DISCOVER_MEM_STATS 114: TMSCHEMA_ANALYTICS_AIMETADATA 115: DISCOVER_OBJECT_COUNTERS
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the discover event.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTPROCESSID = 36  # Contains the process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Contains the session ID associated with the discover event.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the discover event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with the event.
    SERVERNAME = 43  # Contains the name of the instance on which the discover event occurred.
    REQUESTPROPERTIES = (
        45  # Contains the XML for Analysis (XMLA) request properties associated with the discover event.
    )


class DiscoverEndColumns(IntEnum):
    EVENTCLASS = 0  # Contains the event class; this is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class. The following are valid Sub Class Id/Sub Class Name value pairs: 0: DBSCHEMA_CATALOGS 1: DBSCHEMA_TABLES 2: DBSCHEMA_COLUMNS 3: DBSCHEMA_PROVIDER_TYPES 4: MDSCHEMA_CUBES 5: MDSCHEMA_DIMENSIONS 6: MDSCHEMA_HIERARCHIES 7: MDSCHEMA_LEVELS 8: MDSCHEMA_MEASURES 9: MDSCHEMA_PROPERTIES 10: MDSCHEMA_MEMBERS 11: MDSCHEMA_FUNCTIONS 12: MDSCHEMA_ACTIONS 13: MDSCHEMA_SETS 14: DISCOVER_INSTANCES 15: MDSCHEMA_KPIS 16: MDSCHEMA_MEASUREGROUPS 17: MDSCHEMA_COMMANDS 18: DMSCHEMA_MINING_SERVICES 19: DMSCHEMA_MINING_SERVICE_PARAMETERS 20: DMSCHEMA_MINING_FUNCTIONS 21: DMSCHEMA_MINING_MODEL_CONTENT 22: DMSCHEMA_MINING_MODEL_XML 23: DMSCHEMA_MINING_MODELS 24: DMSCHEMA_MINING_COLUMNS 25: DISCOVER_DATASOURCES 26: DISCOVER_PROPERTIES 27: DISCOVER_SCHEMA_ROWSETS 28: DISCOVER_ENUMERATORS 29: DISCOVER_KEYWORDS 30: DISCOVER_LITERALS 31: DISCOVER_XML_METADATA 32: DISCOVER_TRACES 33: DISCOVER_TRACE_DEFINITION_PROVIDERINFO 34: DISCOVER_TRACE_COLUMNS 35: DISCOVER_TRACE_EVENT_CATEGORIES 36: DMSCHEMA_MINING_STRUCTURES 37: DMSCHEMA_MINING_STRUCTURE_COLUMNS 38: DISCOVER_MASTER_KEY 39: MDSCHEMA_INPUT_DATASOURCES 40: DISCOVER_LOCATIONS 41: DISCOVER_PARTITION_DIMENSION_STAT 42: DISCOVER_PARTITION_STAT 43: DISCOVER_DIMENSION_STAT 44: MDSCHEMA_MEASUREGROUP_DIMENSIONS 45: DISCOVER_XEVENT_PACKAGES 46: DISCOVER_XEVENT_OBJECTS 47: DISCOVER_XEVENT_OBJECT_COLUMNS 48: DISCOVER_XEVENT_SESSION_TARGETS 49: DISCOVER_XEVENT_SESSIONS 50: DISCOVER_STORAGE_TABLES 51: DISCOVER_STORAGE_TABLE_COLUMNS 52: DISCOVER_STORAGE_TABLE_COLUMN_SEGMENTS 53: DISCOVER_CALC_DEPENDENCY 54: DISCOVER_CSDL_METADATA 55: DISCOVER_RESOURCE_POOLS 56: TMSCHEMA_MODEL 57: TMSCHEMA_DATA_SOURCES 58: TMSCHEMA_TABLES 59: TMSCHEMA_COLUMNS 60: TMSCHEMA_ATTRIBUTE_HIERARCHIES 61: TMSCHEMA_PARTITIONS 62: TMSCHEMA_RELATIONSHIPS 63: TMSCHEMA_MEASURES 64: TMSCHEMA_HIERARCHIES 65: TMSCHEMA_LEVELS 67: TMSCHEMA_TABLE_STORAGES 68: TMSCHEMA_COLUMN_STORAGES 69: TMSCHEMA_PARTITION_STORAGES 70: TMSCHEMA_SEGMENT_MAP_STORAGES 71: TMSCHEMA_DICTIONARY_STORAGES 72: TMSCHEMA_COLUMN_PARTITION_STORAGES 73: TMSCHEMA_RELATIONSHIP_STORAGES 74: TMSCHEMA_RELATIONSHIP_INDEX_STORAGES 75: TMSCHEMA_ATTRIBUTE_HIERARCHY_STORAGES 76: TMSCHEMA_HIERARCHY_STORAGES 77: DISCOVER_RING_BUFFERS 78: TMSCHEMA_KPIS 79: TMSCHEMA_STORAGE_FOLDERS 80: TMSCHEMA_STORAGE_FILES 81: TMSCHEMA_SEGMENT_STORAGES 82: TMSCHEMA_CULTURES 83: TMSCHEMA_OBJECT_TRANSLATIONS 84: TMSCHEMA_LINGUISTIC_METADATA 85: TMSCHEMA_ANNOTATIONS 86: TMSCHEMA_PERSPECTIVES 87: TMSCHEMA_PERSPECTIVE_TABLES 88: TMSCHEMA_PERSPECTIVE_COLUMNS 89: TMSCHEMA_PERSPECTIVE_HIERARCHIES 90: TMSCHEMA_PERSPECTIVE_MEASURES  95: TMSCHEMA_SETS 96: TMSCHEMA_PERSPECTIVE_SETS 97: TMSCHEMA_EXTENDED_PROPERTIES 98: TMSCHEMA_EXPRESSIONS 99: TMSCHEMA_COLUMN_PERMISSIONS 100: TMSCHEMA_DETAIL_ROWS_DEFINITIONS 101: TMSCHEMA_RELATED_COLUMN_DETAILS 102: TMSCHEMA_GROUP_BY_COLUMNS 103: TMSCHEMA_CALCULATION_GROUPS 104: TMSCHEMA_CALCULATION_ITEMS 105: TMSCHEMA_ALTERNATE_OF_DEFINITIONS 106: TMSCHEMA_REFRESH_POLICIES 107: DISCOVER_POWERBI_DATASOURCES 108: TMSCHEMA_FORMAT_STRING_DEFINITIONS 109: DISCOVER_M_EXPRESSIONS 110: TMSCHEMA_POWERBI_ROLES 111: TMSCHEMA_QUERY_GROUPS 112: DISCOVER_DB_MEM_STATS 113: DISCOVER_MEM_STATS 114: TMSCHEMA_ANALYTICS_AIMETADATA 115: DISCOVER_OBJECT_COUNTERS
    CURRENTTIME = 2  # Contains the current time of the discover event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Contains the time (if available) at which the discover end event started.. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Contains the time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Contains the approximate amount of time (milliseconds) taken by the discover event.
    CPUTIME = 6  # Contains the amount of CPU time (in milliseconds) used by the event.
    SEVERITY = 22  # Contains the severity level of an exception.
    SUCCESS = 23  # Contains the success or failure of the discover event. Values are: 0 = Failure 1 = Success
    ERROR = 24  # Contains the error number of any error associated the discover event.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the discover event.
    DATABASENAME = 28  # Contains the name of the database in which the discover event occurred.
    NTUSERNAME = 32  # Contains the Windows user name associated with the object permission event.
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTPROCESSID = 36  # Contains the client process ID of the application that initiated the event.
    APPLICATIONNAME = 37  # Contains the name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Contains the session ID associated with the discover event.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the discover end event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with the event.
    SERVERNAME = 43  # Contains the name of the instance on which the discover event occurred.
    REQUESTPROPERTIES = 45  # Contains the properties in the XMLA request.


class ServerStateDiscoverBeginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class: 1: DISCOVER_CONNECTIONS 2: DISCOVER_SESSIONS 3: DISCOVER_TRANSACTIONS 6: DISCOVER_DB_CONNECTIONS 7: DISCOVER_JOBS 8: DISCOVER_LOCKS 12: DISCOVER_PERFORMANCE_COUNTERS 13: DISCOVER_MEMORYUSAGE 14: DISCOVER_JOB_PROGRESS 15: DISCOVER_MEMORYGRANT
    CURRENTTIME = 2  # Contains the current time of the server state discover event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Contains the time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the server state discover event.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTPROCESSID = 36  # Contains the process ID of the client application that created the connection to the server.
    APPLICATIONNAME = 37  # Contains the name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Contains the session ID associated with the server state discover event.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the server state discover event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with the event.
    SERVERNAME = 43  # Contains the name of the instance on which the server state discover event occurred.
    REQUESTPROPERTIES = 45  # Contains the properties of the current XMLA request.


class ServerStateDiscoverDataColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class: 1: DISCOVER_CONNECTIONS 2: DISCOVER_SESSIONS 3: DISCOVER_TRANSACTIONS 6: DISCOVER_DB_CONNECTIONS 7: DISCOVER_JOBS 8: DISCOVER_LOCKS 12: DISCOVER_PERFORMANCE_COUNTERS 13: DISCOVER_MEMORYUSAGE 14: DISCOVER_JOB_PROGRESS 15: DISCOVER_MEMORYGRANT
    CURRENTTIME = 2  # Contains the current time of the server state discover event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Contains the time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the server state discover event.
    SESSIONID = 39  # Contains the session ID associated with the server state discover event.
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the server state discover event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with server response to the discover request.
    SERVERNAME = 43  # Contains the name of the instance on which the server state discover event occurred.


class ServerStateDiscoverEndColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class: 1: DISCOVER_CONNECTIONS 2: DISCOVER_SESSIONS 3: DISCOVER_TRANSACTIONS 6: DISCOVER_DB_CONNECTIONS 7: DISCOVER_JOBS 8: DISCOVER_LOCKS 12: DISCOVER_PERFORMANCE_COUNTERS 13: DISCOVER_MEMORYUSAGE 14: DISCOVER_JOB_PROGRESS 15: DISCOVER_MEMORYGRANT
    CURRENTTIME = 2  # Contains the current time of the server state discover event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Contains the time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Contains the time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Contains the amount of time (in milliseconds) taken by the event.
    CPUTIME = 6  # Contains the amount of CPU time (in milliseconds) used by the server state discover event.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the server state discover event.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTPROCESSID = 36  # Contains the process ID of the client application that initiated the XMLA request.
    APPLICATIONNAME = 37  # Contains the name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Contains the Windows domain account associated with the server state discover event.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the server state discover event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with server response to the discover request.
    SERVERNAME = 43  # Contains the name of the instance on which the server state discover event occurred.


class ErrorEventColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    STARTTIME = 3  # Contains the time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    SESSIONTYPE = 8  # Contains the type of the entity that caused the error.
    SEVERITY = 22  # Contains the severity level of an exception associated with the error event. Values are: 0 = Success 1 = Informational 2 = Warning 3 = Error
    SUCCESS = 23  # Contains the success or failure of the error event. Values are: 0 = Failure 1 = Success
    ERROR = 24  # Contains the error number of any error associated with the error event.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the error event.
    DATABASENAME = 28  # Contains the name of the Analysis Services instance on which the error event occurred.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Contains the name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # Contains the process ID of the client application.
    APPLICATIONNAME = 37  # Contains the name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the error event. The SPID directly corresponds to the session GUID used by XML for Analysis (XMLA).
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the error event. The SPID directly corresponds to the session GUID used by XML for Analysis (XMLA).
    TEXTDATA = 42  # Contains the text data associated with the error event.
    SERVERNAME = (
        43  # Contains the name of the server running Analysis Services instance on which the error event occurred.
    )


class FileLoadBeginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class FileLoadEndColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Amount of time (in milliseconds) taken by the event.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    INTEGERDATA = 10  # Integer data.
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class FileSaveBeginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event


class FileSaveEndColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Amount of time (in milliseconds) taken by the event.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    INTEGERDATA = 10  # Integer data.
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class PageOutBeginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class PageOutEndColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Amount of time (in milliseconds) taken by the event.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    INTEGERDATA = 10  # Integer data.
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class PageInBeginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class PageInEndColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Amount of time (in milliseconds) taken by the event.
    JOBID = 7  # Job ID for progress.
    SESSIONTYPE = 8  # Session type (what entity caused the operation).
    INTEGERDATA = 10  # Integer data.
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    SESSIONID = 39  # Session GUID.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class DeadlockColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class LockTimeoutColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Amount of time (in milliseconds) taken by the event.
    INTEGERDATA = 10  # Integer data.
    OBJECTTYPE = 12  # Object type.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    SESSIONID = 39  # Session GUID.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    SERVERNAME = 43  # Name of the server producing the event.


class LockAcquiredColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Unique connection ID.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Session GUID.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class LockReleasedColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Unique connection ID.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Session GUID.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class LockWaitingColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Unique connection ID.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Session GUID.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class AuditLoginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    CONNECTIONID = 25  # Unique connection ID.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SERVERNAME = 43  # Name of the server producing the event.


class AuditLogoutColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Amount of time (in milliseconds) taken by the event.
    CPUTIME = 6  # Amount of CPU time (in milliseconds) used by the event.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    CONNECTIONID = 25  # Unique connection ID.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SERVERNAME = 43  # Name of the server producing the event.


class AuditServerStartsAndStopsColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class: 1: Instance Shutdown 2: Instance Started 3: Instance Paused 4: Instance Continued
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class AuditObjectPermissionEventColumns(IntEnum):
    OBJECTID = 11  # Object ID (note this is a string).
    OBJECTTYPE = 12  # Object type.
    OBJECTNAME = 13  # Object name.
    OBJECTPATH = 14  # Object path. A comma-separated list of parents, starting with the object's parent.
    OBJECTREFERENCE = 15  # Object reference. Encoded as XML for all parents, using tags to describe the object.
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Session GUID.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class AuditAdminOperationsEventColumns(IntEnum):
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class: 1: Backup 2: Restore 3: Synchronize 4: Detach 5: Attach 6: ImageLoad 7: ImageSave
    SEVERITY = 22  # Severity level of an exception.
    SUCCESS = 23  # 1 = success. 0 = failure (for example, a 1 means success of a permissions check and a 0 means a failure of that check).
    ERROR = 24  # Error number of a given event.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Session GUID.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.


class NotificationColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class. The following Sub Class Id: Sub Class Name pairs are defined: 0: Proactive Caching Begin 1: Proactive Caching End 2: Flight Recorder Started 3: Flight Recorder Stopped 4: Configuration Properties Updated 5: SQL Trace 6: Object Created 7: Object Deleted 8: Object Altered 9: Proactive Caching Polling Begin 10: Proactive Caching Polling End 11: Flight Recorder Snapshot Begin 12: Flight Recorder Snapshot End 13: Proactive Caching: notifiable object updated 14: Lazy Processing: start processing 15: Lazy Processing: processing complete 16: SessionOpened Event Begin 17: SessionOpened Event End 18: SessionClosing Event Begin 19: SessionClosing Event End 20: CubeOpened Event Begin 21: CubeOpened Event End 22: CubeClosing Event Begin 23: CubeClosing Event End 24: Transaction abort requested
    CURRENTTIME = 2  # Contains the current time of the notification event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Contains the time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Contains the time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Contains the amount of time (in milliseconds) taken by the event.
    INTEGERDATA = 10  # Contains the integer data associated with the notification event. When the EventSubclass column is 8, values are: 1 = Created 2 = Deleted 3 = Changed object's properties 4 = Changed properties of the object's children 6 = Children added 7 = Children deleted 8 = Object fully processed 9 = Object partially processed 10 = Object unprocessed 11 = Object fully optimized 12 = Object partially optimized 13 = Object not optimized
    OBJECTID = 11  # Contains the Object ID for which this notification is issued; this is a string value.
    OBJECTTYPE = 12  # Contains the object type associated with the notification event.
    OBJECTNAME = 13  # Contains the object name associated with the notification event.
    OBJECTPATH = 14  # Contains the object path associated with the notification event. The path is returned as a comma-separated list of parents, starting with the object's parent.
    OBJECTREFERENCE = 15  # Contains the object reference for the progress report end event. The object reference is encoded as XML by all parents by using tags to describe the object.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the notification event.
    DATABASENAME = 28  # Contains the name of the database in which the notification event occurred.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    SESSIONID = 39  # Contains the session ID associated with the notification event.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the notification event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with the notification event.
    SERVERNAME = 43  # Contains the name of the Analysis Services instance on which the notification event occurred.
    REQUESTPROPERTIES = 45  # Contains the properties of the XMLA request.


class UserDefinedColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # A specific user event subclass that provides additional information about each event class.
    CURRENTTIME = 2  # Contains the current time of the notification event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    INTEGERDATA = 10  # A specific user defined event information.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the notification event.
    DATABASENAME = 28  # Contains the name of the database in which the notification event occurred.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    SESSIONID = 39  # Contains the session ID associated with the notification event.
    NTCANONICALUSERNAME = 40  # Contains the Windows user name associated with the notification event. The user name is in canonical form. For example, engineering.microsoft.com/software/user.
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the notification event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with the notification event.
    SERVERNAME = 43  # Contains the name of the Analysis Services instance on which the notification event occurred.


class QueryBeginColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class. 0: MDXQuery 1: DMXQuery 2: SQLQuery 3: DAXQuery
    CURRENTTIME = 2  # Contains the current time of the event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Contains the time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the query event.
    DATABASENAME = 28  # Contains the name of the database in which the query is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTPROCESSID = 36  # Contains the process ID of the client application.
    APPLICATIONNAME = 37  # Contains the name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Contains the session unique ID of the XMLA request.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the query event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with the query event.
    SERVERNAME = 43  # Contains the name of the instance on which the query event occurred.
    REQUESTPARAMETERS = (
        44  # Contains the parameters for parameterized queries and commands associated with the query event.
    )
    REQUESTPROPERTIES = 45  # Contains the properties of the XMLA request.


class QueryEndColumns(IntEnum):
    EVENTCLASS = 0  # Event Class is used to categorize events.
    EVENTSUBCLASS = 1  # Event Subclass provides additional information about each event class. 0: MDXQuery 1: DMXQuery 2: SQLQuery 3: DAXQuery
    CURRENTTIME = 2  # Contains the current time of the event, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Contains the time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    ENDTIME = 4  # Contains the time at which the event ended. This column is not populated for starting event classes, such as SQL:BatchStarting or SP:Starting. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Contains the amount of elapsed time (in milliseconds) taken by the event.
    CPUTIME = 6  # Contains the amount of CPU time (in milliseconds) used by the event.
    SEVERITY = 22  # Contains the severity level of an exception associated with the query event. Values are: 0 = Success 1 = Informational 2 = Warning 3 = Error
    SUCCESS = 23  # Contains the success or failure of the query event. Values are: 0 = Failure 1 = Success
    ERROR = 24  # Contains the error number of any error associated with the query event.
    CONNECTIONID = 25  # Contains the unique connection ID associated with the query event.
    DATABASENAME = 28  # Contains the name of the database in which the query is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTPROCESSID = 36  # Contains the process ID of the client application.
    APPLICATIONNAME = 37  # Contains the name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SESSIONID = 39  # Contains the session unique ID of the XMLA request.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Contains the server process ID (SPID) that uniquely identifies the user session associated with the query event. The SPID directly corresponds to the session GUID used by XMLA.
    TEXTDATA = 42  # Contains the text data associated with the query event.
    SERVERNAME = 43  # Contains the name of the instance on which the query event occurred.


class ExistingConnectionColumns(IntEnum):
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Unique connection ID.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    SERVERNAME = 43  # Name of the server producing the event.


class ExistingSessionColumns(IntEnum):
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    DURATION = 5  # Amount of time (in milliseconds) taken by the event.
    CPUTIME = 6  # Amount of CPU time (in milliseconds) used by the event.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.
    REQUESTPROPERTIES = 45  # XMLA request properties.


class SessionInitializeColumns(IntEnum):
    CURRENTTIME = 2  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    STARTTIME = 3  # Time at which the event started, when available. For filtering, expected formats are 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS'.
    CONNECTIONID = 25  # Unique connection ID.
    DATABASENAME = 28  # Name of the database in which the statement of the user is running.
    NTUSERNAME = 32  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service  Principal Name (SPN) (appid@tenantid) - Power BI Service Account  (Power BI Service) - Power BI Service on behalf of a UPN or SPN (Power BI Service (UPN/SPN))
    NTDOMAINNAME = 33  # Contains the domain name associated with the user account that triggered the command event.  - Windows domain name for Windows user accounts - AzureAD for Microsoft Entra accounts - NT AUTHORITY accounts without a Windows domain name, such as the Power BI service
    CLIENTHOSTNAME = 35  # Name of the computer on which the client is running. This data column is populated if the host name is provided by the client.
    CLIENTPROCESSID = 36  # The process ID of the client application.
    APPLICATIONNAME = 37  # Name of the client application that created the connection to the server. This column is populated with the values passed by the application rather than the displayed name of the program.
    NTCANONICALUSERNAME = 40  # Contains the user name associated with the command event. Depending on the environment, the user name is in the following form: - Windows user account (DOMAIN\UserName) - User Principal Name (UPN) (username@domain.com) - Service Principal Name (SPN) (appid@tenantid) - Power BI Service Account (Power BI Service)
    SPID = 41  # Server process ID. This uniquely identifies a user session. This directly corresponds to the session GUID used by XML/A.
    TEXTDATA = 42  # Text data associated with the event.
    SERVERNAME = 43  # Name of the server producing the event.
    REQUESTPROPERTIES = 45  # XMLA request properties.


class CommandBeginColumns(IntEnum):
    EVENTCLASS = 0
    EVENTSUBCLASS = 1
    CURRENTTIME = 2
    STARTTIME = 3
    SESSITON = 8
    CONNECTIONID = 25
    DATABASENAME = 28
    NTUSERNAME = 32
    NTDOMAINNAME = 33
    CLIENTPROCESSID = 36
    APPLICATIONNAME = 37
    SESSIONID = 39
    NTCANONICALUSERNAME = 40
    SPID = 41
    TEXTDATA = 42
    SERVERNAME = 43
    REQUESTPARAMETERS = 44
    REQUESTPROPERTIES = 45
    ACTIVITYID = 46
    REQUESTID = 47
    USEROBJECTID = 51
    APPLICATIONCONTEXT = 52
    DATABASEFRIENDLYNAME = 54
    IDENTITY = 55


class CommandEndColumns(IntEnum):
    EVENTCLASS = 0
    EVENTSUBCLASS = 1
    CURRENTTIME = 2
    STARTTIME = 3
    ENDTIME = 4
    DURATION = 5
    CPUTIME = 6
    SESSITON = 8
    INTEGERDATA = 10
    SEVERITY = 22
    SUCCESS = 23
    ERROR = 24
    CONNECTIONID = 25
    DATABASENAME = 28
    NTUSERNAME = 32
    NTDOMAINNAME = 33
    CLIENTPROCESSID = 36
    APPLICATIONNAME = 37
    SESSIONID = 39
    NTCANONICALUSERNAME = 40
    SPID = 41
    TEXTDATA = 42
    SERVERNAME = 43
    ACTIVITYID = 46
    REQUESTID = 47
    ERRORTYPE = 49
    USEROBJECTID = 51
    APPLICATIONCONTEXT = 52
    DATABASEFRIENDLYNAME = 54
    IDENTITY = 55


event_column_mapping = {
    TraceEvents.AUDIT_ADMIN_OPERATIONS_EVENT: AuditAdminOperationsEventColumns,
    TraceEvents.AUDIT_LOGIN: AuditLoginColumns,
    TraceEvents.AUDIT_LOGOUT: AuditLogoutColumns,
    TraceEvents.AUDIT_OBJECT_PERMISSION_EVENT: AuditObjectPermissionEventColumns,
    TraceEvents.AUDIT_SERVER_STARTS_AND_STOPS: AuditServerStartsAndStopsColumns,
    TraceEvents.COMMAND_BEGIN: CommandBeginColumns,
    TraceEvents.COMMAND_END: CommandEndColumns,
    TraceEvents.DEADLOCK: DeadlockColumns,
    TraceEvents.DISCOVER_BEGIN: DiscoverBeginColumns,
    TraceEvents.DISCOVER_END: DiscoverEndColumns,
    TraceEvents.ERROR: ErrorEventColumns,
    TraceEvents.EXISTING_CONNECTION: ExistingConnectionColumns,
    TraceEvents.EXISTING_SESSION: ExistingSessionColumns,
    TraceEvents.FILE_SAVE_BEGIN: FileSaveBeginColumns,
    TraceEvents.FILE_SAVE_END: FileSaveEndColumns,
    TraceEvents.FILE_LOAD_BEGIN: FileLoadBeginColumns,
    TraceEvents.FILE_LOAD_END: FileLoadEndColumns,
    TraceEvents.LOCK_ACQUIRED: LockAcquiredColumns,
    TraceEvents.LOCK_RELEASED: LockReleasedColumns,
    TraceEvents.LOCK_TIMEOUT: LockTimeoutColumns,
    TraceEvents.LOCK_WAITING: LockWaitingColumns,
    TraceEvents.NOTIFICATION: NotificationColumns,
    TraceEvents.PAGEIN_BEGIN: PageInBeginColumns,
    TraceEvents.PAGEIN_END: PageInEndColumns,
    TraceEvents.PAGEOUT_BEGIN: PageOutBeginColumns,
    TraceEvents.PAGEOUT_END: PageOutEndColumns,
    TraceEvents.QUERY_BEGIN: QueryBeginColumns,
    TraceEvents.QUERY_END: QueryEndColumns,
    TraceEvents.SERVER_STATE_DISCOVER_BEGIN: ServerStateDiscoverBeginColumns,
    TraceEvents.SERVER_STATE_DISCOVER_DATA: ServerStateDiscoverDataColumns,
    TraceEvents.SERVER_STATE_DISCOVER_END: ServerStateDiscoverEndColumns,
    TraceEvents.SESSION_INITIALIZE: SessionInitializeColumns,
    TraceEvents.USER_DEFINED: UserDefinedColumns,
}
