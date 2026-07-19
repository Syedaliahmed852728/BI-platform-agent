# Purchase Order Reference

Primary Table

AI_PO_Data

Primary Date

Order_Date

Vendor

Vendor_Name

Item SKU

ItemID

Order Date

Order_Date

Due Date

Due_Date

Received Date

PO_Rec_Date

Ordered Quantity

PO_Ordered_Qty

Received Quantity

PO_Rec_Qty

Pending Quantity

PO_Qty_On_Order

Days Overdue

Days_Overdue

Internal Identifier

Id

Internal Company Identifier

Company_Id

Order Status

Derived from PO_Rec_Date

Pending

PO_Rec_Date IS NULL

Received

PO_Rec_Date IS NOT NULL

Overdue

PO_Rec_Date IS NULL

AND

Days_Overdue > 0