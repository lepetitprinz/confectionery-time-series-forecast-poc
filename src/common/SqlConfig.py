
class SqlConfig(object):
    # Item Master Table
    @staticmethod
    def sql_item_master():
        sql = f"""
            SELECT PROJECT_CD
                 , ITEM_CD
                 , ITEM_NM
              FROM M4S_I002040
            """
        return sql

    # Customer Master Table
    @staticmethod
    def sql_cust_master():
        sql = f"""
            SELECT PROJECT_CD
                 , CUST_CD
                 , CUST_NM
              FROM M4S_I002060
            """
        return sql

    # D
    @staticmethod
    def sql_comm_master():
        sql = f"""
            SELECT OPTION_CD
                 , OPTION_VAL
            FROM M4S_I001020
           WHERE 1=1
             AND MDL_CD = 'DF'
        """
        return sql

    # SELL-IN Table
    @staticmethod
    def sql_sell_in(**kwargs):
        sql = f""" 
            SELECT DIVISION_CD
                 , SOLD_CUST_GRP_CD
                 , SALES.ITEM_CD
                 , BIZ_CD
                 --, BIZ_NM
                 , LINE_CD
                 --, LINE_NM
                 , BRAND_CD
                 --, BRAND_NM
                 , ITEM_CTGR_CD
                 --, ITEM_CTGR_NM
                 , YYMMDD
                 , SEQ
                 , FROM_DC_CD
                 , SALES.UNIT_PRICE
                 , SALES.UNIT_CD
                 , DISCOUNT
                 , WEEK
                 , QTY
                 , CREATE_DATE
              FROM (
                    SELECT PROJECT_CD
                         , DIVISION_CD
                         , SOLD_CUST_GRP_CD
                         , ITEM_CD
                         , YYMMDD
                         , SEQ
                         , FROM_DC_CD
                         , UNIT_PRICE
                         , UNIT_CD
                         , DISCOUNT
                         , WEEK
                         , RST_SALES_QTY AS QTY
                         , CREATE_DATE
                      FROM M4S_I002170
                     WHERE 1=1
                       AND YYMMDD BETWEEN {kwargs['date_from']} AND {kwargs['date_to']}
                    ) SALES
              LEFT OUTER JOIN (
                               SELECT ITEM.PROJECT_CD
                                    , ITEM.ITEM_CD
                                    , ITEM.ITEM_ATTR01_CD AS BIZ_CD
                                    , COMM1.COMM_DTL_CD_NM AS BIZ_NM
                                    , ITEM.ITEM_ATTR02_CD AS LINE_CD
                                    , COMM2.COMM_DTL_CD_NM AS LINE_NM
                                    , ITEM.ITEM_ATTR03_CD AS BRAND_CD
                                    , COMM3.COMM_DTL_CD_NM AS BRAND_NM
                                    , ITEM.ITEM_ATTR04_CD AS ITEM_CTGR_CD
                                    , COMM4.COMM_DTL_CD_NM AS ITEM_CTGR_NM
                                 FROM M4S_I002040 ITEM
                                 LEFT OUTER JOIN M4S_I002011 COMM1
                                   ON ITEM.PROJECT_CD = COMM1.PROJECT_CD
                                  AND ITEM.ITEM_ATTR01_CD = COMM1.COMM_DTL_CD
                                 LEFT OUTER JOIN M4S_I002011 COMM2
                                   ON ITEM.PROJECT_CD = COMM2.PROJECT_CD
                                  AND ITEM.ITEM_ATTR02_CD = COMM2.COMM_DTL_CD
                                 LEFT OUTER JOIN M4S_I002011 COMM3
                                   ON ITEM.PROJECT_CD = COMM3.PROJECT_CD
                                  AND ITEM.ITEM_ATTR03_CD = COMM3.COMM_DTL_CD
                                 LEFT OUTER JOIN M4S_I002011 COMM4
                                   ON ITEM.PROJECT_CD = COMM4.PROJECT_CD
                                  AND ITEM.ITEM_ATTR04_CD = COMM4.COMM_DTL_CD
                               ) ITEM
                ON SALES.PROJECT_CD = ITEM.PROJECT_CD
               AND SALES.ITEM_CD = ITEM.ITEM_CD
               """
        return sql

    # SELL-OUT Table
    @staticmethod
    def sql_sell_out(**kwargs):
        sql = f""" 
            SELECT DIVISION_CD
                 , SOLD_CUST_GRP_CD
                 , SALES.ITEM_CD
                 , BIZ_CD
                 --, BIZ_NM
                 , LINE_CD
                 --, LINE_NM
                 , BRAND_CD
                 --, BRAND_NM
                 , ITEM_CTGR_CD
                 --, ITEM_CTGR_NM
                 , YYMMDD
                 , SEQ
                 , DISCOUNT
                 , WEEK
                 , QTY
                 , CREATE_DATE
              FROM (
                   SELECT PROJECT_CD
                        , DIVISION_CD
                        , SOLD_CUST_GRP_CD
                        , ITEM_CD
                        , YYMMDD
                        , SEQ
                        , DISCOUNT
                        , WEEK
                        , RST_SALES_QTY AS QTY
                        , CREATE_DATE
                   FROM M4S_I002173
                   WHERE 1 = 1
                     AND YYMMDD BETWEEN {kwargs['date_from']} AND {kwargs['date_to']} 
                   ) SALES
              LEFT OUTER JOIN (
                               SELECT ITEM.PROJECT_CD
                                    , ITEM.ITEM_CD
                                    , ITEM.ITEM_ATTR01_CD AS BIZ_CD
                                    , COMM1.COMM_DTL_CD_NM AS BIZ_NM
                                    , ITEM.ITEM_ATTR02_CD AS LINE_CD
                                    , COMM2.COMM_DTL_CD_NM AS LINE_NM
                                    , ITEM.ITEM_ATTR03_CD AS BRAND_CD
                                    , COMM3.COMM_DTL_CD_NM AS BRAND_NM
                                    , ITEM.ITEM_ATTR04_CD AS ITEM_CTGR_CD
                                    , COMM4.COMM_DTL_CD_NM AS ITEM_CTGR_NM
                                 FROM M4S_I002040 ITEM
                                 LEFT OUTER JOIN M4S_I002011 COMM1
                                   ON ITEM.PROJECT_CD = COMM1.PROJECT_CD
                                  AND ITEM.ITEM_ATTR01_CD = COMM1.COMM_DTL_CD
                                 LEFT OUTER JOIN M4S_I002011 COMM2
                                   ON ITEM.PROJECT_CD = COMM2.PROJECT_CD
                                  AND ITEM.ITEM_ATTR02_CD = COMM2.COMM_DTL_CD
                                 LEFT OUTER JOIN M4S_I002011 COMM3
                                   ON ITEM.PROJECT_CD = COMM3.PROJECT_CD
                                  AND ITEM.ITEM_ATTR03_CD = COMM3.COMM_DTL_CD
                                 LEFT OUTER JOIN M4S_I002011 COMM4
                                   ON ITEM.PROJECT_CD = COMM4.PROJECT_CD
                                  AND ITEM.ITEM_ATTR04_CD = COMM4.COMM_DTL_CD
                               ) ITEM
                           ON SALES.PROJECT_CD = ITEM.PROJECT_CD
                          AND SALES.ITEM_CD = ITEM.ITEM_CD
                          """
        return sql

    @staticmethod
    def sql_unit_map():
        sql = """
            SELECT BOX.ITEM_CD
                 , CONVERT(INT, BOX.FAC_PRICE / BOL.FAC_PRICE) AS BOX_BOL
                 , CONVERT(INT, BOX.FAC_PRICE / EA.FAC_PRICE) AS BOX_EA
              FROM (
                    SELECT PROJECT_CD
                         , ITEM_CD
                         , PRICE_START_YYMMDD
                         , FAC_PRICE
                    FROM M4S_I002041
                   WHERE 1=1
                     AND PRICE_QTY_UNIT_CD = 'BOX'
                     AND FAC_PRICE <> 0
                    ) BOX
              LEFT OUTER JOIN (
                               SELECT PROJECT_CD
                                    , ITEM_CD
                                    , PRICE_START_YYMMDD
                                    , FAC_PRICE
                                 FROM M4S_I002041
                                WHERE 1=1
                                  AND PRICE_QTY_UNIT_CD = 'BOL'
                                  AND FAC_PRICE <> 0
                              ) BOL
                ON BOX.PROJECT_CD = BOL.PROJECT_CD
               AND BOX.ITEM_CD = BOL.ITEM_CD
               AND BOX.PRICE_START_YYMMDD = BOL.PRICE_START_YYMMDD
              LEFT OUTER JOIN (
                               SELECT PROJECT_CD
                                    , ITEM_CD
                                    , PRICE_START_YYMMDD
                                    , FAC_PRICE
                                 FROM M4S_I002041
                                WHERE 1=1
                                  AND PRICE_QTY_UNIT_CD = 'EA'
                                  AND FAC_PRICE <> 0
                               ) EA
                ON BOX.PROJECT_CD = EA.PROJECT_CD
               AND BOX.ITEM_CD = EA.ITEM_CD
               AND BOX.PRICE_START_YYMMDD = EA.PRICE_START_YYMMDD
        """
        return sql

    @staticmethod
    def sql_algorithm(**kwargs):
        sql = f"""
            SELECT LOWER(STAT) AS MODEL
                 , INPUT_POINT AS INPUT_WIDTH
                 , PERIOD AS LABEL_WIDTH
              FROM M4S_I103010
             WHERE 1=1
               AND USE_YN = 'Y'
               AND DIVISION = '{kwargs['division']}'           
        """
        return sql

    @staticmethod
    def sql_best_hyper_param_grid():
        sql = """
            SELECT STAT
                 , OPTION_CD
                 , OPTION_VAL
              FROM M4S_I103011
        """
        return sql