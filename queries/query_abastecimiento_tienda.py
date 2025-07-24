def get_abastecimiento_tienda(fecha_inicio: str, fecha_fin: str) -> str:
   query = f"""
    SELECT
    	dd.shipmentdocument,
    	dd.shipmentdocument_type,
    	dd.shipmentdocument_datetime,
    	dd.load_number,
    	dd.transport_rut,
    	tc.transport_alias,
    	dd.trailer_number,
    	dd.driver_rut,
    	dd.driver_name,
    	dd.do_wms,
    	dd.doc_nbr,
    	dd.order_type,
    	dd.order_created_timestamp,
    	dddd.origin_facility_id,
    	dddd.destination_facility_id,
    	dd.shipped_date_time,
    	dd.customerordernbr,
    	dd.item_id,
    	dd.product_class_id,
    	dd.merchandizing_group,
    	dd.merchandizing_type,
    	dd.quantity,
    	dd.size_id,
    	dd.dccenternbr,
    	dd.client_rut,
    	dd.client_name,
    	dd.destination_address,
    	dd.regciucom,
    	dd.cod_reg,
    	dd.cod_ciu,
    	dd.cod_com,
    	dd.fcompromiso,
    	dhd.transport_order_id,
    	tod.rear_seal,
    	tod.side_seal,
    	tod.promised_datetime,
    	CASE
    		WHEN dhd.transport_order_id IS NULL THEN 'To Created'
    		WHEN tod.transport_order_status_id = 0 THEN 'Created'
    		WHEN tod.transport_order_status_id = 1 THEN 'On Floor'
    		WHEN tod.transport_order_status_id = 2 THEN 'Dispatched'
    		WHEN tod.transport_order_status_id = 3 THEN 'Returned'
    		ELSE CAST(tod.transport_order_status_id AS CHAR)
    	END AS to_status,
    	CASE
    		WHEN dddd.status_id IS NULL THEN 'Sin Status'
    		WHEN dddd.status_id = 1 THEN 'En Proceso'
    		WHEN dddd.status_id = 5 THEN 'Impreso/Embarcado'
    		WHEN dddd.status_id = 9 THEN 'Recibido'
    		ELSE CAST(dddd.status_id AS CHAR)
    	END AS jda_status
    FROM scp.doc_dtls dd
    LEFT JOIN scp.doc_dtl_deliveries_dts dddd ON dddd.load_number = dd.load_number
    LEFT JOIN scp.doc_hdr_dts dhd ON dd.load_number = dhd.load_number
    LEFT JOIN scp.transport_orders_dts tod ON tod.id = dhd.transport_order_id
    LEFT JOIN scp.transport_companies tc ON tc.transport_rut = REPLACE(dd.transport_rut, '-', '')
    WHERE
    	dd.shipmentdocument_datetime BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
    	AND dd.order_type IN ('Stock', 'Stock Paris', 'CrossDock')
    	AND dddd.destination_facility_id NOT IN ('012', '046', '050', '100', '180', '215', '400','500', '501', '600')
    	AND dddd.destination_facility_id <> '031'
    	AND tc.transport_alias <> 'CENCOSUD'
    """
   
   return query