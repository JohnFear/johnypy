#!/usr/bin/python

__all__ = ['dbcconst']

dbcconst = {
    'header': 'VERSION ""\nNS_ :\n NS_DESC_\n CM_\n BA_DEF_\n BA_\n VAL_\n CAT_DEF_\n CAT_\n FILTER\n BA_DEF_DEF_\n EV_DATA_\n ENVVAR_DATA_\n SGTYPE_\n SGTYPE_VAL_\n BA_DEF_SGTYPE_\n BA_SGTYPE_\n SIG_TYPE_REF_\n VAL_TABLE_\n SIG_GROUP_\n SIG_VALTYPE_\n SIGTYPE_VALTYPE_\n BO_TX_BU_\n BA_DEF_REL_\n BA_REL_\n BA_DEF_DEF_REL_\n BU_SG_REL_\n BU_EV_REL_\n BU_BO_REL_\n SG_MUL_VAL_\nBS_:\nBU_:\n',
    'attributeDef': 'BA_DEF_ SG_  "SPN" INT 0 524287;\nBA_DEF_  "DBName" STRING ;\nBA_DEF_  "BusType" STRING ;\nBA_DEF_  "ProtocolType" STRING ;\nBA_DEF_ BO_  "VFrameFormat" ENUM  "StandardCAN","ExtendedCAN","reserved","J1939PG";\nBA_DEF_DEF_  "SPN" 0;\nBA_DEF_DEF_  "DBName" "";\nBA_DEF_DEF_  "BusType" "CAN";\nBA_DEF_DEF_  "ProtocolType" "J1939";\nBA_DEF_DEF_  "VFrameFormat" "J1939PG";\n',
    'footer': '\n',
    'msgType': 'Vector__XXX'
}
