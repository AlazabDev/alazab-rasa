---
title: Default module
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"

---

# Default module

Base URLs:

* <a href="https://{{subdomain}}.daftra.com/api2">Production: https://{{subdomain}}.daftra.com/api2</a>

* <a href="">Cloud Mock: </a>

* <a href="https://{{subdomain}}.daftra.com/v2/api/entity">v2: https://{{subdomain}}.daftra.com/v2/api/entity</a>

# Authentication

- HTTP Authentication, scheme: bearer

# API v1 Endpoints/Auth

## POST Generate Access Token

POST /v2/oauth/token

> Body Parameters

```yaml
client_secret: jCfy6cMh1X6NTxR3OWLuvEFa0si5uZKr05UeoAEs
client_id: "1"
grant_type: password
username: "{{username}}"
password: "{{password}}"

```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|body|body|object| no |none|
|» client_secret|body|string| yes |none|
|» client_id|body|string| yes |none|
|» grant_type|body|string| yes |none|
|» username|body|string| yes |none|
|» password|body|string| yes |none|

> Response Examples

> 200 Response

```json
{
    "token_type": "Bearer",
    "expires_in": 94694400,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMjA3MzU4MzdkNjdiNWJjYmMzZGRjMTE4NjJiOThjNWE1ZTBkYzdkNWE3ODliNmE3NmI1MjY3MjZiZWU3M2RlYjA5ZWQ1MWRiNzBkZDdmMWQiLCJpYXQiOjE3NDQ2MjA5MjIuMjU4NzM5OSwiZXhwIjoxODM5MzE1MzgyLjI0NjM3Miwic3ViIjoiNDA2MzI3MSIsInNjb3BlcyI6W10sInByb3ZpZGVyIjoib3duZXIiLCJuYmYiOjE3NDQ1MzQ1ODIuMjU4NzU4MX0.QBCnITMq1eIcdr0jx3JkJxU3QzB-PGPCAF0bKLbDOUmQf_o_XGUoEkLTQen75aBM9faIteUrfCwxZ4I8h_LoB-eprQK4Qxg-pbTLOoEixv6WMKTGL_AwCVpuWFoPWbSKVRDb43yFqGoLHuKLBe9-3I2fIjlXguvGbODaECEeL-cJkab6-oqlidiH9dpB-hFqQv1Nsd3uQUxu6C5PJDFyI1si10xy80Hu3jlMX7OS2V8SkFhsq11l2xTgHDDsXf9z4spp3di7dUzoXgFPFoXlp47zGRvc8kNLkr8_Dz3omttPsm82mKZNsCwAatac6Fxw7PJlHjTaTmSukHx9YAd9Nuc6q_AZ_7y2YhvYBj1DhxeVLb-i2BlxXTTJYgjZhqgLvh--4Z5XZCiXv2tagSKggNhNIoKKDftsEDYY8_5fWddMOeRI085yuB5vyrNrnGmv4E8_9VQI43nGuUyVWOFp5EvfQSPB8Db0byG95aSl9ub2d2Akclt3aZ9fWgV3Agxu34x6EQ1YGBrwoHJ_0XvUOWhI3T4_N1lmQapnpVhAEfvyVKccS1jAFO18OvKN-depxYzNIkkbnrxZ9uEsRpsj44oJlSt8QYKKSDn1t9gObkRWLqdmltgayskP4F1Rm2OE-b3FagG_IeKUyua5SFtsi_EU4JP37Kz2yqJWF5yW4R0",
    "refresh_token": "def50200fcb939ed9b9d75a0a9193135250cc7efe5248a55c62715c22b0b38fe68c039f2fa1dcdf1d1ea6d45b29729506558341783734dc0360ea6de5190281cd068c5e1a9a5a1c1d540de5c888e7727d6fa46087726ff6566774230a252dce8952c46bbc80100033d01768f6fe6c0b4ca9425f9b5442b0ecb748fcd7d157a52ec2486746723134052e276d760e333bd6177b30cbd0bd744f9aacde79ba65522298e49decc5194e03b683804176f116626cc8897399fa46996e7f5bc2c5946583c8787dcfd6e28f7febc6aa9fea4468b01e2c0d3ee52ff89cf14446a962544a8a58448082c0bb2e9e4bcf007f734a5b68334d1a1bb029402ad11f2c067425e60787ea467ca9547f7de03edbfa74264b362b34fdcef74b7cc383e4cda7a32b080a9dee0be786c62260960e33a87850156fb64ce9bcdb0fbbb0d72475c1268b6e8fb3de85643e6b5e5ef205fa0e3016a37f9408f01ebcfd020d9cb71c147578cd2f8bd4f14b241cf301a"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» token_type|string|false|none||none|
|» expires_in|integer|false|none||none|
|» access_token|string|false|none||none|
|» refresh_token|string|false|none||none|

# API v1 Endpoints/Invoices

## GET GET All Invoices

GET /invoices{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |20|
|page|query|integer| no |1|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Invoice": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Invoice|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Invoice

POST /invoices{format}

> Body Parameters

```json
{
    "Invoice": {
        "staff_id": 0,
        "subscription_id": 26,
        "store_id": 0,
        "no": "0700000AAAAA0001",
        "po_number": "26",
        "name": "Darrel Gusikowski-Koch",
        "branch_id": 1,
        "client_id": 15,
        "is_offline": true,
        "currency_code": "USD",
        "client_business_name": "Example Client",
        "client_first_name": "Example",
        "client_last_name": "Client",
        "client_email": "client@example.com",
        "client_address1": "Florida West Damionworth Warren County 19902 Schmitt Wells Suite 780",
        "client_address2": "West Virginia South Sandrine Union County 681 Huels Branch Apt. 308",
        "client_postal_code": "29515-2869",
        "client_city": "Santiagocester",
        "client_state": "Vermont",
        "client_country_code": "EG",
        "date": "2018-11-07",
        "draft": false,
        "discount": 0,
        "discount_amount": 0,
        "deposit": 0,
        "deposit_type": 0,
        "notes": "fugiat Ut",
        "html_notes": "voluptate nulla",
        "invoice_layout_id": 1,
        "estimate_id": 0,
        "shipping_options": 2,
        "shipping_amount": null,
        "client_active_secondary_address": false,
        "client_secondary_name": "Steven Zulauf",
        "client_secondary_address1": "Wyoming Lake Leilani Franklin County 39823 Jefferson Street Suite 706",
        "client_secondary_address2": "Oregon Dibbertbury Hamilton County 8594 Clark Street Suite 780",
        "client_secondary_city": "North Shyanne",
        "client_secondary_state": "Florida",
        "client_secondary_postal_code": "00967",
        "client_secondary_country_code": "CC",
        "follow_up_status": null,
        "work_order_id": null,
        "requisition_delivery_status": 2,
        "pos_shift_id": null,
        "qr_code_url": "https://yoursite.daftra.com/qr/?d64=QVE1TmIyaGhiV1ZrSUVGemFISmhaZ0lJTVRFMU16WTJRMUlERkRJd01qSXRNVEF0TWpoVU1EQTZNREU2TVRWYUJBRXdCUUV3",
        "invoice_html_url": "https://yoursite.daftra.com/invoices/preview/2621?hash=c06543fe13bd4850b521733687c53259",
        "invoice_pdf_url": "https://yoursite.daftra.com/invoices/view/2621.pdf?hash=c06543fe13bd4850b521733687c53259"
    },
    "InvoiceItem": [
        {
            "item": "occaecat",
            "description": "Arto vesco sumptus cinis laudantium subito spoliatio admoveo. Vulticulus cruciamentum eveniet denuo tabgo. Usitas ultio vinum alius teres adfectus confero utilis.",
            "unit_price": 77.59,
            "quantity": 1,
            "tax1": null,
            "tax2": null,
            "product_id": 12,
            "col_3": null,
            "col_4": null,
            "col_5": null,
            "discount": 0,
            "discount_type": 2,
            "store_id": 0,
            "lot": [
                586865858
            ],
            "expiry_date": [
                "2024-09-29"
            ],
            "serials": []
        }
    ],
    "Payment": [
        {
            "payment_method": "ad elit Ut dolor adipisicing",
            "amount": 561.89,
            "transaction_id": "payment",
            "treasury_id": -16127808,
            "date": "2025-03-24 21:22:32",
            "staff_id": -86060770
        },
        {
            "payment_method": "ad elit Ut dolor adipisicing",
            "amount": 561.89,
            "transaction_id": "payment",
            "treasury_id": -16127808,
            "date": "2025-03-24 21:22:32",
            "staff_id": -86060770
        }
    ],
    "InvoiceCustomField": {},
    "Deposit": {},
    "InvoiceReminder": {},
    "Document": {},
    "DocumentTitle": {}
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» Invoice|body|object| yes |none|
|»» staff_id|body|integer| yes |none|
|»» subscription_id|body|integer| yes |none|
|»» store_id|body|integer| yes |none|
|»» no|body|string| yes |none|
|»» po_number|body|string| yes |none|
|»» name|body|string| yes |none|
|»» branch_id|body|integer| no |Branch. [GET General Listing API with model `Branch`](/24700082e0)|
|»» client_id|body|integer| yes |none|
|»» is_offline|body|boolean| yes |none|
|»» currency_code|body|string| yes |none|
|»» client_business_name|body|string| yes |none|
|»» client_first_name|body|string| yes |none|
|»» client_last_name|body|string| yes |none|
|»» client_email|body|string| yes |none|
|»» client_address1|body|string| yes |none|
|»» client_address2|body|string| yes |none|
|»» client_postal_code|body|string| yes |none|
|»» client_city|body|string| yes |none|
|»» client_state|body|string| yes |none|
|»» client_country_code|body|string| yes |none|
|»» date|body|string| yes |none|
|»» draft|body|boolean| yes |none|
|»» discount|body|integer| yes |none|
|»» discount_amount|body|integer| yes |none|
|»» deposit|body|integer| yes |none|
|»» deposit_type|body|integer| yes |none|
|»» notes|body|string| yes |none|
|»» html_notes|body|string| yes |none|
|»» invoice_layout_id|body|integer| yes |none|
|»» estimate_id|body|integer| yes |none|
|»» shipping_options|body|integer| yes |none|
|»» shipping_amount|body|null| yes |none|
|»» client_active_secondary_address|body|boolean| yes |none|
|»» client_secondary_name|body|string| yes |none|
|»» client_secondary_address1|body|string| yes |none|
|»» client_secondary_address2|body|string| yes |none|
|»» client_secondary_city|body|string| yes |none|
|»» client_secondary_state|body|string| yes |none|
|»» client_secondary_postal_code|body|string| yes |none|
|»» client_secondary_country_code|body|string| yes |none|
|»» follow_up_status|body|integer| yes |none|
|»» work_order_id|body|null| yes |none|
|»» requisition_delivery_status|body|integer| yes |none|
|»» pos_shift_id|body|integer| yes |none|
|»» qr_code_url|body|string| yes |none|
|»» invoice_html_url|body|string| yes |none|
|»» invoice_pdf_url|body|string| yes |none|
|» InvoiceItem|body|[object]| yes |none|
|»» invoice_id|body|integer| no |none|
|»» item|body|string| no |none|
|»» description|body|string| no |none|
|»» unit_price|body|number| no |none|
|»» quantity|body|integer| no |none|
|»» tax1|body|integer| no |none|
|»» tax2|body|integer| no |none|
|»» product_id|body|integer| no |none|
|»» col_3|body|null| no |none|
|»» col_4|body|null| no |none|
|»» col_5|body|null| no |none|
|»» discount|body|number| no |none|
|»» discount_type|body|integer| no |none|
|»» store_id|body|integer| no |none|
|» Payment|body|[object]| yes |none|
|»» payment_method|body|string| yes |none|
|»» amount|body|number| yes |none|
|»» transaction_id|body|string| yes |none|
|»» treasury_id|body|integer| yes |none|
|»» date|body|string| yes |none|
|»» staff_id|body|integer| yes |none|
|» InvoiceCustomField|body|object| yes |none|
|» Deposit|body|object| yes |none|
|» InvoiceReminder|body|object| yes |none|
|» Document|body|object| yes |none|
|» DocumentTitle|body|object| yes |none|
|» *anonymous*|body|object| no |none|
|»» Invoice|body|object| no |none|
|»»» id|body|integer(int64)| no |Unique identifier|
|»»» staff_id|body|integer(int64)| no |Staff ID who created the invoice get it from [GET STAFF API](/15115375e0) if it's `0` that means the site owner is the staff that created it|
|»»» subscription_id|body|integer(int64)¦null| no |Invoice id which this invoice follows so when adding refund this field indicates which invoice is being refunded get the invoice ids from [GET All Invoices API](/15115241e0) when this field is set to `null` that means that this invoice isn't a child of any invoice|
|»»» store_id|body|integer(int64)| yes |The store which this invoice uses get it from [GET STORE API](/15115366e0)|
|»»» type|body|integer(int64)| no |invoice type|
|»»» no|body|string¦null| no |Invoice number, this field is auto generated but can be overridden|
|»»» po_number|body|string¦null| no |Purchase invoice number|
|»»» name|body|string¦null| no |used in template and subscription only|
|»»» client_id|body|integer(int64)| yes |The client id get it from [GET Client API](/15115261e0)|
|»»» is_offline|body|boolean| no |!! 0 / 1 indicates if the client is offline|
|»»» currency_code|body|string| no |Currency Code|
|»»» client_business_name|body|string| no |Client's business name|
|»»» client_first_name|body|string| no |Client's first name|
|»»» client_last_name|body|string| no |Client's last name|
|»»» client_email|body|string(email)| no |Client's email|
|»»» client_address1|body|string| no |Client's Address line 1|
|»»» client_address2|body|string| no |Client's Address line 2|
|»»» client_postal_code|body|string| no |Client's postal code|
|»»» client_city|body|string| no |Client's City|
|»»» client_state|body|string| no |Client's State|
|»»» client_country_code|body|string| no |Client's country ISO "ALPHA-2" Code|
|»»» date|body|string(date)| no |the date of the invoice|
|»»» payment_status|body|integer¦null| no |payment status, on adding invoice this field is set automatically via invoice payments|
|»»» draft|body|boolean| no |[0 => not draft,1 => draft]|
|»»» discount|body|double| no |discount percentage of the invoice ```note that this field alternate with `discount_amount```` example to set 5% discount is set this field to 5 and `discount_amount` field to 0|
|»»» discount_amount|body|double| no |absolute discount of the invoice ```note that this field alternate with `discount```` example to set 5 USD discount is set this field to 5 and `discount` field to 0|
|»»» deposit|body|double| no |Deposit amount|
|»»» deposit_type|body|integer| no |Deposit Type|
|»»» summary_subtotal|body|double| no |total invoice without taxes|
|»»» summary_discount|body|double| no |total discount applied on the invoice|
|»»» summary_total|body|double| no |total invoice with taxes|
|»»» summary_paid|body|double| no |total paid amount|
|»»» summary_unpaid|body|double| no |total unpaid amount|
|»»» summary_deposit|body|double| no |total deposited amount|
|»»» summary_refund|body|double| no |total refunded amount|
|»»» notes|body|string| no |Notes for the client|
|»»» html_notes|body|string| no |html template notes|
|»»» created|body|date-time| no |the date when the invoice was created|
|»»» modified|body|date-time| no |the last date when the invoice was modified|
|»»» invoice_layout_id|body|integer(int64)¦null| no |the layout for viewing this invoice get it from [GET General Listing API with model `InvoiceLayout`](/15115384e0) if not set the default layout is used|
|»»» estimate_id|body|integer(int64)| no |The estimate of this invoice get it from [GET Estimates API](/15115246e0) if it's not set the primary store is used|
|»»» shipping_options|body|integer| no |Deposit Type|
|»»» shipping_amount|body|double¦null| no |Deposit amount|
|»»» client_active_secondary_address|body|boolean| no |0/1 if the secondary data is active|
|»»» client_secondary_name|body|string| no |Supplier's name|
|»»» client_secondary_address1|body|string| no |Client's address line 1|
|»»» client_secondary_address2|body|string| no |Client's address line 2|
|»»» client_secondary_city|body|string| no |Client's City|
|»»» client_secondary_state|body|string| no |Client's State|
|»»» client_secondary_postal_code|body|string| no |Client's postal code|
|»»» client_secondary_country_code|body|string| no |Client's country ISO "ALPHA-2" Code|
|»»» follow_up_status|body|integer¦null| no |Follow Up Status get it from [GET Follow up statuses with model invoice](/15115383e0)|
|»»» work_order_id|body|integer¦null| no |Work Order ID get it from [GET Work orders](/15115271e0)|
|»»» requisition_delivery_status|body|integer¦null| no |Requisition delivery Status|
|»»» pos_shift_id|body|integer¦null| no |POS session id|
|»»» source_type|body|integer¦null| no |Source type that created the invoice if it's `null` then this means the invoice has no source|
|»»» source_id|body|integer¦null| no |source item id that created the invoice|
|»»» qr_code_url|body|string| no |direct url for the QR Code image of that invoice for KSA Electronic Invoice only|
|»»» invoice_html_url|body|string| no |direct url that will return HTML code of the invoice|
|»»» invoice_pdf_url|body|string| no |direct url to download pdf version of the invoice|
|» *anonymous*|body|any| no |none|
|» *anonymous*|body|any| no |none|
|» *anonymous*|body|any| no |none|
|» *anonymous*|body|any| no |none|
|» *anonymous*|body|any| no |none|
|» *anonymous*|body|any| no |none|
|» *anonymous*|body|any| no |none|

#### Enum

|Name|Value|
|---|---|
|»»» type|0 => Invoice|
|»»» type|2 => Subscription|
|»»» type|3 => Estimate|
|»»» type|5 => Credit Note|
|»»» type|6 => Refund Receipt|
|»»» type|7 => BNR|
|»»» type|8 => Booking|
|»»» payment_status|null => Unpaid|
|»»» payment_status|'' => Unpaid|
|»»» payment_status|0 => Unpaid|
|»»» payment_status|1 => Partially Paid|
|»»» payment_status|2 => Paid|
|»»» payment_status|3 => Refunded|
|»»» payment_status|4 => OverPaid|
|»»» payment_status|-1 => Draft|
|»»» deposit_type|0 => Unpaid|
|»»» deposit_type|1 => Unpaid|
|»»» deposit_type|2 => Paid|
|»»» shipping_options|'' => Auto|
|»»» shipping_options|1 => Don't show shipping options|
|»»» shipping_options|2 => Show the main client details|
|»»» shipping_options|3 => Show secondary client details|
|»»» requisition_delivery_status|1 => Pending|
|»»» requisition_delivery_status|2 => Not All Available|
|»»» requisition_delivery_status|3 => Accepted|
|»»» requisition_delivery_status|4 => Cancelled|
|»»» requisition_delivery_status|5 => Modified|
|»»» source_type|0 => Invoice|
|»»» source_type|2 => Subscription|
|»»» source_type|3 => Estimate|
|»»» source_type|5 => Credit Note|
|»»» source_type|6 => Refund Receipt|
|»»» source_type|7 => BNR|
|»»» source_type|8 => Booking|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Invoice

GET /invoices/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Invoice": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Invoice|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Invoices

PUT /invoices/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Invoices

DELETE /invoices/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Estimates

## GET GET All Estimates

GET /estimates{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Estimate": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Estimate|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Estimate

POST /estimates{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Estimate

GET /estimates/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Estimate": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Estimate|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Estimates

PUT /estimates/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Estimates

DELETE /estimates/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Credit Notes

## GET GET All Credit Notes

GET /credit_notes{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "CreditNote": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» CreditNote|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Credit Note

POST /credit_notes{format}

> Body Parameters

```json
{
  "CreditNote": null,
  "InvoiceItem": [
    {
      "invoice_id": 0,
      "item": "string",
      "description": "string",
      "unit_price": 0.1,
      "quantity": 0,
      "tax1": 0,
      "tax2": 0,
      "product_id": 0,
      "col_3": null,
      "col_4": null,
      "col_5": null,
      "discount": 0.1,
      "discount_type": "1 => Percentage",
      "store_id": 0
    }
  ]
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Credit Note

GET /credit_notes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "CreditNote": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» CreditNote|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Credit Notes

PUT /credit_notes/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Credit Notes

DELETE /credit_notes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Refund Receipts

## GET GET All Refund Receipts

GET /refund_receipts{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "RefundReceipt": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» RefundReceipt|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Refund Receipt

POST /refund_receipts{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Refund Receipt

GET /refund_receipts/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "RefundReceipt": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» RefundReceipt|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Refund Receipts

PUT /refund_receipts/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Refund Receipts

DELETE /refund_receipts/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Clients

## GET GET All Clients

GET /clients{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|integer| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Client": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Client|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Client

POST /clients{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Client

GET /clients/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Client": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Client|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Clients

PUT /clients/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Clients

DELETE /clients/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Suppliers

## GET GET All Suppliers

GET /suppliers{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Supplier": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Supplier|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Supplier

POST /suppliers{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Supplier

GET /suppliers/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Supplier": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Supplier|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Suppliers

PUT /suppliers/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Suppliers

DELETE /suppliers/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Work Orders

## GET GET Single Work Order

GET /work_orders/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Operation|Inline|

### Responses Data Schema

## PUT Edit Work Orders

PUT /work_orders/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Work Orders

DELETE /work_orders/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET All Work Orders

GET /work_orders{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "WorkOrder": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» WorkOrder|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Work Order

POST /work_orders{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Client Appointments

## GET GET All Client Appointments

GET /client_appointments{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "ClientAppointment": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» ClientAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Client Appointment

POST /client_appointments{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Client Appointment

GET /client_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "ClientAppointment": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» ClientAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Client Appointments

PUT /client_appointments/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Client Appointments

DELETE /client_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Invoice Appointments

## GET GET All Invoice Appointments

GET /invoice_appointments{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "InvoiceAppointment": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» InvoiceAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Invoice Appointment

POST /invoice_appointments{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Invoice Appointment

GET /invoice_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "InvoiceAppointment": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» InvoiceAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Invoice Appointments

PUT /invoice_appointments/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Invoice Appointments

DELETE /invoice_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Estimate Appointments

## GET GET All Estimate Appointments

GET /estimate_appointments{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "EstimateAppointment": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» EstimateAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Estimate Appointment

POST /estimate_appointments{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Estimate Appointment

GET /estimate_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "EstimateAppointment": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» EstimateAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Estimate Appointments

PUT /estimate_appointments/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Estimate Appointments

DELETE /estimate_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Work Order Appointments

## GET GET All Work Order Appointments

GET /work_order_appointments{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "WorkOrderAppointment": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» WorkOrderAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Work Order Appointment

POST /work_order_appointments{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Work Order Appointment

GET /work_order_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "WorkOrderAppointment": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» WorkOrderAppointment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Work Order Appointments

PUT /work_order_appointments/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Work Order Appointments

DELETE /work_order_appointments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Notes

## GET GET All Notes

GET /notes{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Note": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Note|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Note

GET /notes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Note": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Note|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Notes

PUT /notes/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Notes

DELETE /notes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Note

POST /notes/{type}/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|type|path|string| yes |none|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Time Tracking

## GET GET All Time Tracking

GET /time_tracking{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "TimeTracking": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» TimeTracking|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Time Tracking

POST /time_tracking{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Time Tracking

GET /time_tracking/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "TimeTracking": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» TimeTracking|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Time Tracking

PUT /time_tracking/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Time Tracking

DELETE /time_tracking/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Invoice Payments

## GET GET All Invoice Payments

GET /invoice_payments{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "InvoicePayment": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» InvoicePayment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Invoice Payment

POST /invoice_payments{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Invoice Payment

GET /invoice_payments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "InvoicePayment": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» InvoicePayment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Invoice Payments

PUT /invoice_payments/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Invoice Payments

DELETE /invoice_payments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Client Payments

## GET GET All Client Payments

GET /client_payments{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "ClientPayment": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» ClientPayment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Client Payment

POST /client_payments{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Client Payment

GET /client_payments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "ClientPayment": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» ClientPayment|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Client Payments

PUT /client_payments/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Client Payments

DELETE /client_payments/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Products

## GET GET All Products

GET /products{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |Show p|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|load_custom_data|query|integer| no |Show products custom data|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Product": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Product|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Product

POST /products{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Product

GET /products/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Product": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Product|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Products

PUT /products/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Products

DELETE /products/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Journals

## GET GET All Journals

GET /journals{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Journal": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Journal|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Journal

POST /journals{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Journal

GET /journals/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Journal": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Journal|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Journals

PUT /journals/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Journals

DELETE /journals/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Journal Accounts

## GET GET All Journal Accounts

GET /journal_accounts{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "JournalAccount": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» JournalAccount|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Journal Account

POST /journal_accounts{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Journal Account

GET /journal_accounts/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "JournalAccount": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» JournalAccount|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Journal Accounts

PUT /journal_accounts/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Journal Accounts

DELETE /journal_accounts/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Journal Cats

## GET GET All Journal Cats

GET /journal_cats{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "JournalCat": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» JournalCat|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Journal Cat

POST /journal_cats{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Journal Cat

GET /journal_cats/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "JournalCat": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» JournalCat|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Journal Cats

PUT /journal_cats/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Journal Cats

DELETE /journal_cats/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Expenses

## GET GET All Expenses

GET /expenses{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Expense": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Expense|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Expens

POST /expenses{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Expens

GET /expenses/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Expense": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Expense|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Expenses

PUT /expenses/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Expenses

DELETE /expenses/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Incomes

## GET GET All Incomes

GET /incomes{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Income": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Income|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Income

POST /incomes{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Income

GET /incomes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Income": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Income|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Incomes

PUT /incomes/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Incomes

DELETE /incomes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Taxes

## GET GET All Taxes

GET /taxes{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Tax": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Tax|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Taxe

POST /taxes{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Taxe

GET /taxes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Tax": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Tax|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Taxes

PUT /taxes/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Taxes

DELETE /taxes/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Purchase Invoices

## GET GET All Purchase Invoices

GET /purchase_invoices{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "PurchaseOrder": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» PurchaseOrder|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Purchase Invoice

POST /purchase_invoices{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Purchase Invoice

GET /purchase_invoices/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "PurchaseOrder": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» PurchaseOrder|any|false|none||none|

*allOf*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*and*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|»»» *anonymous*|any|false|none||none|

*continued*

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Purchase Invoices

PUT /purchase_invoices/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Purchase Invoices

DELETE /purchase_invoices/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Purchase Refunds

## GET GET All Purchase Refunds

GET /purchase_refunds{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "PurchaseRefund": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» PurchaseRefund|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Purchase Refund

POST /purchase_refunds{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Purchase Refund

GET /purchase_refunds/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "PurchaseRefund": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» PurchaseRefund|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Purchase Refunds

PUT /purchase_refunds/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Purchase Refunds

DELETE /purchase_refunds/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Stock Transactions

## GET GET All Stock Transactions

GET /stock_transactions{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "StockTransaction": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» StockTransaction|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Stock Transaction

POST /stock_transactions{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Stock Transaction

GET /stock_transactions/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "StockTransaction": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» StockTransaction|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Stock Transactions

PUT /stock_transactions/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Stock Transactions

DELETE /stock_transactions/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Stores

## GET GET All Stores

GET /stores{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Store": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Store|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Store

POST /stores{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Store

GET /stores/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Store": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Store|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Stores

PUT /stores/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Stores

DELETE /stores/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Treasuries

## GET GET All Treasuries

GET /treasuries{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Treasury": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Treasury|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## POST Add New Treasury

POST /treasuries{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Treasury

GET /treasuries/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Treasury": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Treasury|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## PUT Edit Treasuries

PUT /treasuries/{id}{format}

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Treasuries

DELETE /treasuries/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Product Categories

## GET GET All Product Categories

GET /product_categories{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "ProductCategory": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Invalid Category You must send type from the types above|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» ProductCategory|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Product Category

GET /product_categories/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "ProductCategory": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» ProductCategory|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Staff

## GET GET Single Staff

GET /staff/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Staff": null
  },
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Staff|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET All Staff

GET /staff{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|limit|query|integer| no |The collection items limit|
|page|query|integer| no |The collection items page|
|load_custom_data|query|integer| no |Show staff custom data|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    {
      "Staff": null
    }
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[object]|false|none||none|
|»» Staff|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Client-attendance-log

## POST Add New Client-attendance-log

POST /client-attendance-log/store

> Body Parameters

```json
null
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|any| no |none|

> Response Examples

> 202 Response

```json
{
  "code": 202,
  "result": "successful",
  "id": "2415"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Created|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Bad Request|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **202**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» id|integer|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|
|» validation_errors|object|false|none||none|
|»» Attribute that caused the error|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/General Listing

## GET GET General Listing

GET /listing/{model}{format}

Get list data as key,value pairs the key is the item_id and value is its title

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|model|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Listing": {
      "1": "title1",
      "2": "title2"
    }
  }
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Invalid Model You must send Model from the models mentioned above|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Listing|object|false|none||none|
|»»» **additionalProperties**|object|false|none||Item key,value pair|
|»»»» item_id|integer(int32)|false|none||none|
|»»»» title|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v1 Endpoints/Requsitions

## GET GET All Requisitions 

GET /requisitions

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## POST Add New Requisition

POST /requisitions

> Body Parameters

```json
{
    "Requisition": {
        "type": 1,
        "currency_code":"",
        "Status":"",
        "Order_type":"",
        "work_order_id":"",
        "date": "09/11/2025 14:32",
        "store_id": "1",
        "To_store_id":"", 
        "journal_account_id": "",
        "number": "",
        "notes": ""
    },
    "RequisitionItem":[
            {
                "item":"item",
                "product_id":12,
                "org_name": "",
                "unit_price": 1,
                "quantity":1,
                 "lot": [586865858],
                 "expiry_date": ["2024-09-29"],
                 "serials":[]   
            }
        ]
}

```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» Requisition|body|object| yes |none|
|»» type|body|integer| yes |none|
|»» currency_code|body|string| yes |none|
|»» Status|body|string| yes |none|
|»» Order_type|body|string| yes |none|
|»» work_order_id|body|string| yes |none|
|»» date|body|string| yes |none|
|»» store_id|body|string| yes |none|
|»» To_store_id|body|string| yes |none|
|»» journal_account_id|body|string| yes |none|
|»» number|body|string| yes |none|
|»» notes|body|string| yes |none|
|» RequisitionItem|body|[object]| yes |none|
|»» item|body|string| no |none|
|»» product_id|body|integer| no |none|
|»» org_name|body|string| no |none|
|»» unit_price|body|integer| no |none|
|»» quantity|body|integer| no |none|
|»» lot|body|[integer]| no |none|
|»» expiry_date|body|[string]| no |none|
|»» serials|body|[string]| no |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET GET single Requisition

GET /requisitions/{id}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## PUT Edit Requisitions

PUT /requisitions/{id}

> Body Parameters

```json
{
    "Requisition": {
        "type": 1,
        "currency_code": "",
        "Status": "",
        "Order_type": "",
        "work_order_id": "",
        "date": "08/08/2022 14:32",
        "store_id": "1",
        "To_store_id": "",
        "journal_account_id": "",
        "number": "",
        "notes": ""
    },
    "RequisitionItem": [
        {
            "item": "",
            "product_id": "",
            "org_name": "",
            "unit_price": "",
            "quantity": "",
            "lot": [586865858],
            "expiry_date": ["2024-09-29"],
            "serials":[]  
        }
    ]
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## DELETE Delete Requisitions

DELETE /requisitions/{id}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v1 Endpoints/Booking

## POST Add new Booking

POST /bookings/add

> Body Parameters

```json
{
    "InvoiceItem": [
        {
            "product_id": "96"
        }
    ],
    "Invoice": {
        "staff_id": "1",
        "date": "28/09/2025",
        "client_id": "18",
        "description": "",
        "end_time": "23:59",
        "start_time": "00:00",
        "branch_id": 1,
        "converted": 1
    }
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» InvoiceItem|body|[object]| yes |none|
|»» product_id|body|string| no |none|
|» Invoice|body|object| yes |none|
|»» staff_id|body|string| yes |none|
|»» date|body|string| yes |none|
|»» client_id|body|string| yes |none|
|»» description|body|string| yes |none|
|»» end_time|body|string| yes |none|
|»» start_time|body|string| yes |none|
|»» branch_id|body|integer| yes |none|
|»» converted|body|integer| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET Change Booking Status

GET /api2/bookings/change_status/{bookingId}/{bookingStatus}

> Body Parameters

```
string

```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|bookingId|path|string| yes |none|
|bookingStatus|path|string| yes |1: confirmed; 3: canceled; 4: done.|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|string| no |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET Convert booking to Invoice

GET /api2/bookings/convert_to_invoice/{bookingId}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|bookingId|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET Get All Bookings

GET /booking/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET Get Single Booking

GET /booking/{bookingId}/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|bookingId|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## DELETE Delete booking

DELETE /bookings/{bookingId}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|bookingId|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v1 Endpoints/Advance Payment Invoices

## GET GET All Advance payment

GET /invoice/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|filter[type]=19|query|string| no |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET GET Single Advance payment

GET /invoice/{ID}/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|ID|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "id": 361,
    "no": "00015",
    "date": "2026-04-07",
    "staff_id": 0,
    "subscription_id": null,
    "store_id": 1,
    "type": 19,
    "po_number": "26",
    "client_id": 46,
    "is_offline": 1,
    "currency_code": "SAR",
    "client_business_name": "Doaa Abdelfattah",
    "client_first_name": null,
    "client_last_name": null,
    "client_email": "",
    "client_address1": "",
    "client_address2": null,
    "client_postal_code": null,
    "client_city": null,
    "client_state": null,
    "client_country_code": "SAR",
    "payment_status": 2,
    "draft": 0,
    "discount": 0,
    "due_after": 0,
    "issue_date": "2026-04-07",
    "summary_subtotal": 100,
    "summary_discount": 0,
    "summary_total": 100,
    "summary_paid": 100,
    "summary_unpaid": 0,
    "terms_id": null,
    "html_notes": "",
    "created": "2026-04-08 13:55:37",
    "modified": "2026-04-08 13:55:37",
    "required_terms_file": 0,
    "last_sent": null,
    "invoice_layout_id": 9,
    "estimate_id": 0,
    "shipping_option_id": null,
    "summary_refund": 0,
    "client_active_secondary_address": 0,
    "client_secondary_name": null,
    "client_secondary_address1": "",
    "client_secondary_address2": null,
    "client_secondary_city": null,
    "client_secondary_state": null,
    "client_secondary_postal_code": null,
    "client_secondary_country_code": null,
    "follow_up_status": null,
    "source_type": null,
    "source_id": null,
    "sales_person_id": -3,
    "extra_details": "{\"client_balance\":100,\"invoice_version\":2}",
    "discount_amount": 0,
    "shipping_amount": null,
    "work_order_id": null,
    "item_columns": "",
    "branch_id": 1,
    "requisition_delivery_status": null,
    "item_discount_amount": 0,
    "pos_shift_id": null,
    "requisitions": [],
    "adjustment_label": null,
    "adjustment_value": null,
    "order_source_id": null,
    "store": {
        "id": 1,
        "name": "Primary Warehouse",
        "active": 1
    },
    "clients": {
        "id": 46,
        "group_price_id": null,
        "is_offline": 1,
        "client_number": "*DSR202645",
        "staff_id": -3,
        "business_name": "Doaa Abdelfattah",
        "first_name": null,
        "last_name": null,
        "email": null,
        "password": null,
        "address1": "",
        "address2": null,
        "city": null,
        "state": null,
        "postal_code": null,
        "phone1": "+966547895120",
        "phone2": null,
        "country_code": null,
        "notes": null,
        "active_secondary_address": 0,
        "secondary_name": null,
        "secondary_address1": "",
        "secondary_address2": null,
        "secondary_city": null,
        "secondary_state": null,
        "secondary_postal_code": null,
        "secondary_country_code": null,
        "language_code": null,
        "default_currency_code": null,
        "last_login": null,
        "suspend": 0,
        "last_ip": null,
        "created": "2026-03-31 12:32:06",
        "modified": "2026-03-31 12:32:06",
        "follow_up_status": null,
        "category": "",
        "bn1": null,
        "bn1_label": null,
        "bn2_label": null,
        "bn2": null,
        "starting_balance": null,
        "photo": null,
        "birth_date": null,
        "gender": null,
        "map_location": null,
        "type": 2,
        "credit_limit": 0,
        "credit_period": 0,
        "branch_id": 1,
        "national_id": null,
        "attachment": null,
        "category_id": null,
        "secondary_follow_up_status": null,
        "timezone": 0,
        "tags": null,
        "assigned_users": null
    },
    "branch": {
        "id": 1,
        "name": "Main Branch",
        "status": 1,
        "created": "2024-12-10 09:33:10",
        "modified": "2024-12-10 09:33:10"
    },
    "payment": [
        {
            "invoice_id": 361,
            "client_id": null,
            "payment_method": "cash",
            "amount": 100,
            "transaction_id": "",
            "date": "2026-04-07 00:00:00",
            "email": null,
            "status": 1,
            "notes": null,
            "response_code": null,
            "response_message": null,
            "created": "2026-04-08 13:55:39",
            "currency_code": "SAR",
            "first_name": null,
            "last_name": null,
            "address1": "",
            "address2": null,
            "city": null,
            "state": null,
            "postal_code": null,
            "country_code": "SAR",
            "phone1": "+966547895120",
            "phone2": null,
            "attachment": null,
            "staff_id": -3,
            "payment_work_order_id": null,
            "treasury_id": 1,
            "pos_shift_id": null,
            "receipt_notes": null,
            "extra_details": null,
            "branch_id": 1,
            "id": 156,
            "added_by": 1
        }
    ],
    "invoice_item": [
        {
            "invoice_id": 361,
            "item": "خدمة",
            "description": "",
            "unit_price": 100,
            "quantity": 1,
            "tax1": 0,
            "tax2": 0,
            "product_id": 112,
            "col_3": "",
            "col_4": "",
            "col_5": null,
            "discount": null,
            "discount_type": null,
            "store_id": 1,
            "unit_factor": null,
            "unit_small_name": null,
            "unit_name": null,
            "display_order": 0,
            "summary_tax1": 0,
            "summary_tax2": 0,
            "col_6": null,
            "col_7": null,
            "col_8": null,
            "created": "2026-04-08 13:55:38",
            "modified": "2026-04-08 13:55:38",
            "unit_factor_id": null,
            "offer_id": null,
            "tracking_data": "{\"lot\": null, \"serial\": null, \"expiry_date\": null}",
            "serials": null,
            "extra_details": null,
            "calculated_discount": 0,
            "subtotal": 100,
            "id": 556,
            "sales_account_id": null,
            "cost_center_id": null,
            "sales_person_id": null
        }
    ],
    "invoice_documents": [],
    "invoice_custom_fields": [],
    "invoice_client": {
        "id": 46,
        "group_price_id": null,
        "is_offline": 1,
        "client_number": "*DSR202645",
        "staff_id": -3,
        "business_name": "Doaa Abdelfattah",
        "first_name": null,
        "last_name": null,
        "email": null,
        "password": null,
        "address1": "",
        "address2": null,
        "city": null,
        "state": null,
        "postal_code": null,
        "phone1": "+966547895120",
        "phone2": null,
        "country_code": null,
        "notes": null,
        "active_secondary_address": 0,
        "secondary_name": null,
        "secondary_address1": "",
        "secondary_address2": null,
        "secondary_city": null,
        "secondary_state": null,
        "secondary_postal_code": null,
        "secondary_country_code": null,
        "language_code": null,
        "default_currency_code": null,
        "last_login": null,
        "suspend": 0,
        "last_ip": null,
        "created": "2026-03-31 12:32:06",
        "modified": "2026-03-31 12:32:06",
        "follow_up_status": null,
        "category": "",
        "bn1": null,
        "bn1_label": null,
        "bn2_label": null,
        "bn2": null,
        "starting_balance": null,
        "photo": null,
        "birth_date": null,
        "gender": null,
        "map_location": null,
        "type": 2,
        "credit_limit": 0,
        "credit_period": 0,
        "branch_id": 1,
        "national_id": null,
        "attachment": null,
        "category_id": null,
        "secondary_follow_up_status": null,
        "timezone": 0,
        "tags": null,
        "assigned_users": null
    },
    "invoice_layout": {
        "id": 9,
        "field1": "Bill To:",
        "field2": "",
        "field3": "",
        "field4": "",
        "field5": "",
        "image": null,
        "staff_id": 0,
        "html": "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\r\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\r\n\t<head>\r\n\t\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\r\n\t\t<title>Invoice Template</title>\r\n\t</head>\r\n\t<style type=\"text/css\">\r\n\t\t*{ margin:0; padding:0;}\r\n\t\tbody{ background:transparent; font:12px Arial, Helvetica, sans-serif }\r\n\t\t.invoice-wrap{ width:660px; margin:0 auto; background:#FFF; color:#000}\r\n\t\t.invoice-inner{ margin:0 30px; padding:20px 0}\r\n\t\t.invoice-address{border-top: 3px double #000000; margin: 35px 0; padding-top: 25px;}\r\n\t\t bold_title {font-weight:bold;}\r\n\t\t big_title{ font-size:18px; font-weight:100}\r\n\t\t.bussines-name{ font-size:18px; font-weight:100}\r\n\t\t.invoice-name{font-size:22px; font-weight:700}\r\n\t\t.listing-table th{background-color: #e5e5e5;border-bottom: 1px solid #555555;border-top: 1px solid #555555;font-weight: bold; text-align:left; padding:6px 4px}\r\n\t\t.listing-table td{border-bottom: 1px solid #555555; text-align:left; padding:5px 6px; vertical-align:top}\r\n\t\t.total-table td{ border-left: 1px solid #555555;}\r\n\t\t.total-row{ background-color: #e5e5e5;border-bottom: 1px solid #555555;border-top: 1px solid #555555;font-weight: bold;}\r\n\t\t.row-items{ margin:5px 0; display:block}\r\n\t\t.notes-block{ margin:50px 0 0 0}\r\n\t\r\ntr, td, th {\r\n    page-break-inside: avoid !important;\r\n} \r\n                                          \r\n.qr-code img {margin-top:10px}\r\n</style>\r\n\t<body>\r\n\t\t<div class=\"invoice-wrap\">\r\n{%html_sticky_header%}\r\n\t\t\t<div class=\"invoice-inner\">\r\n\t\t\t\t<table width=\"100%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\r\n\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t<td align=\"left\" valign=\"top\">\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t<img id=\"logo\" class='editable-area' src=\"{%logo%}\" width=\"{%logo-width%}\" height=\"{%logo-height%}\"/> \r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t<td align=\"left\" valign=\"top\" >\r\n\t\t\t\t\t\t\t<div id=\"business_info\" class='editable-area'>\r\n\t\t\t\t\t\t\t\t{%business_info%}\r\n\t\t\t\t\t\t\t</div>\r\n\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t<td valign=\"top\" align=\"right\">\r\n\t\t\t\t\t\t\t\t<p id=\"invoice_title\" class=\"editable-area invoice-name\">{%invoice_title%}</p><div class=\"qr-code\">\r\n{%sa_qr_code_image%}<br/>\r\n</div>\r\n\t\t\t\t\t\t</td>\r\n\t\t\t\t\t</tr>\r\n\t\t\t\t</table>\r\n\r\n\t\t\t\t<div class=\"invoice-address\">\r\n\t\t\t\t\t<table width=\"100%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\r\n\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td width=\"50%\" align=\"left\" valign=\"top\">\r\n\t\t\r\n\t\t\t<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\" style=\"float: left;\" ><strong id=\"field1\" class='editable-area'>{%field1%}</strong></td>\r\n\t\t\t\t\t\t\t\t\t\t<td style=\"padding-left:20px;\" valign=\"top\"><div id=\"client_info\" class='editable-area'>{%client_info%}</div></td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n<tr id=\"shipping_options\" style=\"display:none;\">\r\n\t\t\t\t\t\t\t\t\t\t<td valign=\"top\" style=\"float: left;\" ><br/><strong id=\"label_ship\" class='editable-area'>{%label_ship%}</strong></td>\r\n\t\t\t\t\t\t\t\t\t\t<td style=\"padding-left:20px;\" valign=\"top\"><br/><div id=\"ship_info\" class='editable-area'>{%ship_info%}</div></td>\r\n\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t</table>\r\n\t\t\t\t\t\t\t</td>\r\n<td width=\"50%\" valign=\"top\" align=\"right\" >\r\n<table id=\"invoice_basics\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" align=\"right\" >\r\n\r\n<tr>\r\n<td  align=\"right\"><strong class=\"editable-area\" id=\"label_invoice_no\">{%label_invoice_no%}</strong></td>\r\n<td  style=\"padding-left:20px;\" align=\"left\" >{%invoice_number%}\r\n</td>\r\n</tr>\r\n<tr {%refund_invoice_number_condition%}>\r\n                                <td  align=\"right\"><strong class=\"editable-area\" id=\"refund_label_invoice_no\">{%refund_invoice_no_title%}</strong></td>\r\n                                <td  style=\"padding-left:20px;\" align=\"left\" >{%refund_invoice_number%}</td>\r\n                            </tr>\r\n<!-- InvoiceDate -->\r\n<tr>\r\n<td  align=\"right\" ><strong class=\"editable-area\" id=\"label_date\">{%label_date%}</strong></td>\r\n<td style=\"padding-left:20px;\" align=\"left\" >{%invoice_date%}\r\n</td>\r\n</tr>\r\n<!-- /InvoiceDate -->\r\n\r\n</table>\r\n<custom_field id=\"custom_fields\" style=\"clear:both\" class='editable-area'   border=\"0\" cellspacing=\"0\" cellpadding=\"0\" align=\"right\">\r\n{%custom_fields%}\r\n</custom_field>\r\n\r\n\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t</table>\r\n\t\t\t\t</div>\t \r\n\r\n\t\t\t\t<div id=\"items-list\">\r\n\t\t\t\t\t\t{%items_list%}\r\n\t\t\t\t</div>\r\n\r\n\t\t\t\t<div class=\"notes-block\">\r\n\t\t\t\t\t<table width=\"100%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\r\n\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td>\r\n                                                          <div style=\"font-style:italic\" class=\"editable-area\" id=\"footer\">{%footer%}</div>\r\n                                                        </td>\r\n\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t</table>\r\n\r\n\t\t\t\t</div>\r\n\t\t\t\t<br />\r\n\r\n\t\t\t</div>\r\n{%html_sticky_footer%}\r\n\t\t</div>\r\n\t</body>\r\n</html>",
        "invoice_title": "Invoice",
        "estimate_title": "Estimate",
        "creditnote_title": "Credit Note",
        "business_info": "<bold_title>{%business_name%}</bold_title>\r\n{%address1%}\r\n{%city%}، {%state%} {%postal_code%}\r\n{%phone1%}\r\n",
        "logo": "{%logo_site%}",
        "client_info": "{%client_organization%}\r\n{%client_first_name%} {%client_last_name%}\r\n{%client_address%}\r\n{%client_city%} {%client_state%} {%client_postcode%}\r\n{%client_business_registration_info1%} {%client_business_registration_info2%}",
        "label_invoice_no": "Invoice No",
        "label_date": "Invoice Date",
        "label_po_no": "Po No",
        "label_total": "Total",
        "label_status": "Status",
        "label_due_days": "Due After",
        "label_due_date": "Due Date",
        "label_deposit": "Next Payment",
        "label_paid_amount": "Paid",
        "label_unpaid_amount": "Balance Due",
        "label_subtotal": "Subtotal",
        "label_description": "Description",
        "label_item": "Item",
        "label_tax1": null,
        "label_tax2": null,
        "label_quantity": "Quantity",
        "label_unit_price": "Unit Price",
        "label_item_total": "Item Total",
        "label_from_date": "From Date",
        "label_to_date": "To Date",
        "label_discount": "Discount",
        "items_list": "<table cellspacing=\"0\" cellpadding=\"0\" border=\"0\" width=\"100%\" id=\"listing_table\" class=\"listing-table total-table\" style=\" \">\r\n<tr>\r\n<th width=\"\" bgcolor=\"#e5e5e5\" class=\"editable-area\" id=\"label_item\">{%label_item%}</th>\r\n<!-- Description --><th width=\"250\" bgcolor=\"#e5e5e5\" class=\"editable-area\" id=\"label_description\">{%label_description%}</th><!-- /Description -->\r\n<th width=\"60\" bgcolor=\"#e5e5e5\" class=\"editable-area\" id=\"label_unit_price\">{%label_unit_price%}</th>\r\n<th width=\"30\" bgcolor=\"#e5e5e5\" class=\"editable-area\" id=\"label_quantity\">{%label_quantity%}</th>\r\n<th width=\"80\" bgcolor=\"#e5e5e5\" class=\"editable-area\" id=\"label_subtotal\">{%label_subtotal%}</th>\r\n</tr>\r\n<list_items>\r\n{%items%}\r\n</list_items>\r\n<!-- Subtotal --><tr>\r\n\t\t\t\t\t\t\t\t<td style=\"border:none;\" bgcolor=\"#FFF\" colspan=\"{%cols%}\"></td><td style=\"border-left:none;border-right:none;\"  colspan=\"2\" ><strong class=\"editable-area\" id=\"label_item_total\">{%label_item_total%}</strong></td>\r\n\t\t\t\t\t\t\t\t<td style=\"border-left:none;border-right:none;\" align=\"left\">{%value_item_total%}</td>\r\n\t\t\t\t\t\t\t</tr><!-- /Subtotal -->\r\n{%invoice-taxes%}\r\n<tr class=\"total-row\">\r\n<td style=\"border:none;\" bgcolor=\"#FFF\" colspan=\"{%cols%}\"></td>\t\t\t\t\t\t\t\t<td style=\"border-left:none;border-right:none;\"  colspan=\"2\" ><h4><strong class=\"editable-area\" id=\"label_total\">{%label_total%}</strong></h4></td>\r\n\t\t\t\t\t\t\t\t<td style=\"border-left:none;border-right:none;\" align=\"left\">{%value_total%}</td>\r\n\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t<!-- PaidAmount -->\r\n<tr>\r\n<td style=\"border:none;\" bgcolor=\"#FFF\" colspan=\"{%cols%}\"></td>\t\t\t\t\t\t\t\t<td style=\"border-left:none;border-right:none;\"  colspan=\"2\" ><strong class=\"editable-area\" id=\"label_paid_amount\">{%label_paid_amount%}</strong></td>\r\n\t\t\t\t\t\t\t\t<td style=\"border-left:none;border-right:none;\" align=\"left\">{%value_paid_amount%}</td>\r\n\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t<tr>\r\n<td style=\"border:none;\" bgcolor=\"#FFF\" colspan=\"{%cols%}\"></td>\t\t\t\t\t\t\t\t<td style=\"border-left:none;border-right:none;\"  colspan=\"2\" ><strong class=\"editable-area\" id=\"label_unpaid_amount\">{%label_unpaid_amount%}</strong></td>\r\n\t\t\t\t\t\t\t\t<td style=\"border-left:none;border-right:none;\" align=\"left\">{%value_unpaid_amount%}</td>\r\n\t\t\t\t\t\t\t</tr>\r\n<!-- /PaidAmount -->\t\t\t\t\t\t</table>\r\n\t\t\t\t\t\t<div style=\"clear:both; height:1px;\">&nbsp;</div>",
        "custom_fields": "<tr>\r\n\t<td  align=\"right\"><strong class='custom-field-label'>{%label%}</strong></td>\r\n\t<td style=\"padding-left:20px;\" align=\"left\" class='custom-field-value'>{%value%}</td>\r\n</tr>",
        "template_id": 1,
        "footer": "{%invoice_notes%}",
        "created": "2025-07-22 17:29:53",
        "default": 0,
        "default_estimate": 0,
        "default_creditnote": 0,
        "default_refundreceipt": 0,
        "simple_item_currency": 1,
        "show_balance_due": 1,
        "show_ship": 0,
        "label_ship": "Ship To:",
        "ship_info": "{%client_secondary_name%}\r\n{%client_secondary_address%}\r\n{%client_secondary_city%}, {%client_secondary_state%} {%client_secondary_postcode%}",
        "language_id": 41,
        "label_shipping": "Shipping",
        "item_columns": "",
        "footer_html": null,
        "css_style": null,
        "view_style": "{\"font_size\":\"\",\"font_file\":\"\",\"font_variant\":\"\",\"font_name\":\"\",\"font_family\":\"\",\"paper_size\":\"a4\",\"paper_width\":\"\",\"paper_height\":\"\",\"border_color\":\"\",\"header_text_color\":\"\",\"header_bg_color\":\"\",\"odd_bg_color\":\"\",\"even_bg_color\":\"\",\"extra_css\":\"\",\"margin_top\":\"\",\"margin_bottom\":\"\",\"margin_left\":\"\",\"margin_right\":\"\"}",
        "label_creditnote_no": "Credit Note No",
        "label_creditnote_to": null,
        "label_creditnote_date": "Credit Note Date",
        "label_estimate_no": "Estimate No",
        "label_estimate_date": "Estimate Date",
        "refundreceipt_title": "Refund Receipt",
        "quantity_price": "",
        "label_refundreceipt_no": "Refund Receipt No",
        "label_refundreceipt_date": "Refund Date",
        "label_to": "To",
        "label_refunded": "Refunded",
        "alt_template": 0,
        "layout_type": 0,
        "sticky_footer": "",
        "sticky_header": "",
        "default_purchase_refund": 0,
        "default_purchase_order": 0,
        "branch_id": 1,
        "purchase_order_title": null,
        "default_width": 200,
        "default_height": 0,
        "min_width": 0,
        "min_height": 0,
        "max_width": 458,
        "max_height": 200,
        "name": "Template1 English"
    },
    "invoice_installment_agreements": [],
    "invoice_requisitions": [],
    "journal_account_route": [],
    "invoice_appointments": [],
    "staff": null,
    "work_orders": null,
    "pos_shifts": null,
    "invoice_source_order": null,
    "custom_data": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» no|string|true|none||none|
|» date|string|true|none||none|
|» staff_id|integer|true|none||none|
|» subscription_id|null|true|none||none|
|» store_id|integer|true|none||none|
|» type|integer|true|none||none|
|» po_number|string|true|none||none|
|» client_id|integer|true|none||none|
|» is_offline|integer|true|none||none|
|» currency_code|string|true|none||none|
|» client_business_name|string|true|none||none|
|» client_first_name|null|true|none||none|
|» client_last_name|null|true|none||none|
|» client_email|string|true|none||none|
|» client_address1|string|true|none||none|
|» client_address2|null|true|none||none|
|» client_postal_code|null|true|none||none|
|» client_city|null|true|none||none|
|» client_state|null|true|none||none|
|» client_country_code|string|true|none||none|
|» payment_status|integer|true|none||none|
|» draft|integer|true|none||none|
|» discount|integer|true|none||none|
|» due_after|integer|true|none||none|
|» issue_date|string|true|none||none|
|» summary_subtotal|integer|true|none||none|
|» summary_discount|integer|true|none||none|
|» summary_total|integer|true|none||none|
|» summary_paid|integer|true|none||none|
|» summary_unpaid|integer|true|none||none|
|» terms_id|null|true|none||none|
|» html_notes|string|true|none||none|
|» created|string|true|none||none|
|» modified|string|true|none||none|
|» required_terms_file|integer|true|none||none|
|» last_sent|null|true|none||none|
|» invoice_layout_id|integer|true|none||none|
|» estimate_id|integer|true|none||none|
|» shipping_option_id|null|true|none||none|
|» summary_refund|integer|true|none||none|
|» client_active_secondary_address|integer|true|none||none|
|» client_secondary_name|null|true|none||none|
|» client_secondary_address1|string|true|none||none|
|» client_secondary_address2|null|true|none||none|
|» client_secondary_city|null|true|none||none|
|» client_secondary_state|null|true|none||none|
|» client_secondary_postal_code|null|true|none||none|
|» client_secondary_country_code|null|true|none||none|
|» follow_up_status|null|true|none||none|
|» source_type|null|true|none||none|
|» source_id|null|true|none||none|
|» sales_person_id|integer|true|none||none|
|» extra_details|string|true|none||none|
|» discount_amount|integer|true|none||none|
|» shipping_amount|null|true|none||none|
|» work_order_id|null|true|none||none|
|» item_columns|string|true|none||none|
|» branch_id|integer|true|none||none|
|» requisition_delivery_status|null|true|none||none|
|» item_discount_amount|integer|true|none||none|
|» pos_shift_id|null|true|none||none|
|» requisitions|[string]|true|none||none|
|» adjustment_label|null|true|none||none|
|» adjustment_value|null|true|none||none|
|» order_source_id|null|true|none||none|
|» store|object|true|none||none|
|»» id|integer|true|none||none|
|»» name|string|true|none||none|
|»» active|integer|true|none||none|
|» clients|object|true|none||none|
|»» id|integer|true|none||none|
|»» group_price_id|null|true|none||none|
|»» is_offline|integer|true|none||none|
|»» client_number|string|true|none||none|
|»» staff_id|integer|true|none||none|
|»» business_name|string|true|none||none|
|»» first_name|null|true|none||none|
|»» last_name|null|true|none||none|
|»» email|null|true|none||none|
|»» password|null|true|none||none|
|»» address1|string|true|none||none|
|»» address2|null|true|none||none|
|»» city|null|true|none||none|
|»» state|null|true|none||none|
|»» postal_code|null|true|none||none|
|»» phone1|string|true|none||none|
|»» phone2|null|true|none||none|
|»» country_code|null|true|none||none|
|»» notes|null|true|none||none|
|»» active_secondary_address|integer|true|none||none|
|»» secondary_name|null|true|none||none|
|»» secondary_address1|string|true|none||none|
|»» secondary_address2|null|true|none||none|
|»» secondary_city|null|true|none||none|
|»» secondary_state|null|true|none||none|
|»» secondary_postal_code|null|true|none||none|
|»» secondary_country_code|null|true|none||none|
|»» language_code|null|true|none||none|
|»» default_currency_code|null|true|none||none|
|»» last_login|null|true|none||none|
|»» suspend|integer|true|none||none|
|»» last_ip|null|true|none||none|
|»» created|string|true|none||none|
|»» modified|string|true|none||none|
|»» follow_up_status|null|true|none||none|
|»» category|string|true|none||none|
|»» bn1|null|true|none||none|
|»» bn1_label|null|true|none||none|
|»» bn2_label|null|true|none||none|
|»» bn2|null|true|none||none|
|»» starting_balance|null|true|none||none|
|»» photo|null|true|none||none|
|»» birth_date|null|true|none||none|
|»» gender|null|true|none||none|
|»» map_location|null|true|none||none|
|»» type|integer|true|none||none|
|»» credit_limit|integer|true|none||none|
|»» credit_period|integer|true|none||none|
|»» branch_id|integer|true|none||none|
|»» national_id|null|true|none||none|
|»» attachment|null|true|none||none|
|»» category_id|null|true|none||none|
|»» secondary_follow_up_status|null|true|none||none|
|»» timezone|integer|true|none||none|
|»» tags|null|true|none||none|
|»» assigned_users|null|true|none||none|
|» branch|object|true|none||none|
|»» id|integer|true|none||none|
|»» name|string|true|none||none|
|»» status|integer|true|none||none|
|»» created|string|true|none||none|
|»» modified|string|true|none||none|
|» payment|[object]|true|none||none|
|»» invoice_id|integer|false|none||none|
|»» client_id|null|false|none||none|
|»» payment_method|string|false|none||none|
|»» amount|integer|false|none||none|
|»» transaction_id|string|false|none||none|
|»» date|string|false|none||none|
|»» email|null|false|none||none|
|»» status|integer|false|none||none|
|»» notes|null|false|none||none|
|»» response_code|null|false|none||none|
|»» response_message|null|false|none||none|
|»» created|string|false|none||none|
|»» currency_code|string|false|none||none|
|»» first_name|null|false|none||none|
|»» last_name|null|false|none||none|
|»» address1|string|false|none||none|
|»» address2|null|false|none||none|
|»» city|null|false|none||none|
|»» state|null|false|none||none|
|»» postal_code|null|false|none||none|
|»» country_code|string|false|none||none|
|»» phone1|string|false|none||none|
|»» phone2|null|false|none||none|
|»» attachment|null|false|none||none|
|»» staff_id|integer|false|none||none|
|»» payment_work_order_id|null|false|none||none|
|»» treasury_id|integer|false|none||none|
|»» pos_shift_id|null|false|none||none|
|»» receipt_notes|null|false|none||none|
|»» extra_details|null|false|none||none|
|»» branch_id|integer|false|none||none|
|»» id|integer|false|none||none|
|»» added_by|integer|false|none||none|
|» invoice_item|[object]|true|none||none|
|»» invoice_id|integer|false|none||none|
|»» item|string|false|none||none|
|»» description|string|false|none||none|
|»» unit_price|integer|false|none||none|
|»» quantity|integer|false|none||none|
|»» tax1|integer|false|none||none|
|»» tax2|integer|false|none||none|
|»» product_id|integer|false|none||none|
|»» col_3|string|false|none||none|
|»» col_4|string|false|none||none|
|»» col_5|null|false|none||none|
|»» discount|null|false|none||none|
|»» discount_type|null|false|none||none|
|»» store_id|integer|false|none||none|
|»» unit_factor|null|false|none||none|
|»» unit_small_name|null|false|none||none|
|»» unit_name|null|false|none||none|
|»» display_order|integer|false|none||none|
|»» summary_tax1|integer|false|none||none|
|»» summary_tax2|integer|false|none||none|
|»» col_6|null|false|none||none|
|»» col_7|null|false|none||none|
|»» col_8|null|false|none||none|
|»» created|string|false|none||none|
|»» modified|string|false|none||none|
|»» unit_factor_id|null|false|none||none|
|»» offer_id|null|false|none||none|
|»» tracking_data|string|false|none||none|
|»» serials|null|false|none||none|
|»» extra_details|null|false|none||none|
|»» calculated_discount|integer|false|none||none|
|»» subtotal|integer|false|none||none|
|»» id|integer|false|none||none|
|»» sales_account_id|null|false|none||none|
|»» cost_center_id|null|false|none||none|
|»» sales_person_id|null|false|none||none|
|» invoice_documents|[string]|true|none||none|
|» invoice_custom_fields|[string]|true|none||none|
|» invoice_client|object|true|none||none|
|»» id|integer|true|none||none|
|»» group_price_id|null|true|none||none|
|»» is_offline|integer|true|none||none|
|»» client_number|string|true|none||none|
|»» staff_id|integer|true|none||none|
|»» business_name|string|true|none||none|
|»» first_name|null|true|none||none|
|»» last_name|null|true|none||none|
|»» email|null|true|none||none|
|»» password|null|true|none||none|
|»» address1|string|true|none||none|
|»» address2|null|true|none||none|
|»» city|null|true|none||none|
|»» state|null|true|none||none|
|»» postal_code|null|true|none||none|
|»» phone1|string|true|none||none|
|»» phone2|null|true|none||none|
|»» country_code|null|true|none||none|
|»» notes|null|true|none||none|
|»» active_secondary_address|integer|true|none||none|
|»» secondary_name|null|true|none||none|
|»» secondary_address1|string|true|none||none|
|»» secondary_address2|null|true|none||none|
|»» secondary_city|null|true|none||none|
|»» secondary_state|null|true|none||none|
|»» secondary_postal_code|null|true|none||none|
|»» secondary_country_code|null|true|none||none|
|»» language_code|null|true|none||none|
|»» default_currency_code|null|true|none||none|
|»» last_login|null|true|none||none|
|»» suspend|integer|true|none||none|
|»» last_ip|null|true|none||none|
|»» created|string|true|none||none|
|»» modified|string|true|none||none|
|»» follow_up_status|null|true|none||none|
|»» category|string|true|none||none|
|»» bn1|null|true|none||none|
|»» bn1_label|null|true|none||none|
|»» bn2_label|null|true|none||none|
|»» bn2|null|true|none||none|
|»» starting_balance|null|true|none||none|
|»» photo|null|true|none||none|
|»» birth_date|null|true|none||none|
|»» gender|null|true|none||none|
|»» map_location|null|true|none||none|
|»» type|integer|true|none||none|
|»» credit_limit|integer|true|none||none|
|»» credit_period|integer|true|none||none|
|»» branch_id|integer|true|none||none|
|»» national_id|null|true|none||none|
|»» attachment|null|true|none||none|
|»» category_id|null|true|none||none|
|»» secondary_follow_up_status|null|true|none||none|
|»» timezone|integer|true|none||none|
|»» tags|null|true|none||none|
|»» assigned_users|null|true|none||none|
|» invoice_layout|object|true|none||none|
|»» id|integer|true|none||none|
|»» field1|string|true|none||none|
|»» field2|string|true|none||none|
|»» field3|string|true|none||none|
|»» field4|string|true|none||none|
|»» field5|string|true|none||none|
|»» image|null|true|none||none|
|»» staff_id|integer|true|none||none|
|»» html|string|true|none||none|
|»» invoice_title|string|true|none||none|
|»» estimate_title|string|true|none||none|
|»» creditnote_title|string|true|none||none|
|»» business_info|string|true|none||none|
|»» logo|string|true|none||none|
|»» client_info|string|true|none||none|
|»» label_invoice_no|string|true|none||none|
|»» label_date|string|true|none||none|
|»» label_po_no|string|true|none||none|
|»» label_total|string|true|none||none|
|»» label_status|string|true|none||none|
|»» label_due_days|string|true|none||none|
|»» label_due_date|string|true|none||none|
|»» label_deposit|string|true|none||none|
|»» label_paid_amount|string|true|none||none|
|»» label_unpaid_amount|string|true|none||none|
|»» label_subtotal|string|true|none||none|
|»» label_description|string|true|none||none|
|»» label_item|string|true|none||none|
|»» label_tax1|null|true|none||none|
|»» label_tax2|null|true|none||none|
|»» label_quantity|string|true|none||none|
|»» label_unit_price|string|true|none||none|
|»» label_item_total|string|true|none||none|
|»» label_from_date|string|true|none||none|
|»» label_to_date|string|true|none||none|
|»» label_discount|string|true|none||none|
|»» items_list|string|true|none||none|
|»» custom_fields|string|true|none||none|
|»» template_id|integer|true|none||none|
|»» footer|string|true|none||none|
|»» created|string|true|none||none|
|»» default|integer|true|none||none|
|»» default_estimate|integer|true|none||none|
|»» default_creditnote|integer|true|none||none|
|»» default_refundreceipt|integer|true|none||none|
|»» simple_item_currency|integer|true|none||none|
|»» show_balance_due|integer|true|none||none|
|»» show_ship|integer|true|none||none|
|»» label_ship|string|true|none||none|
|»» ship_info|string|true|none||none|
|»» language_id|integer|true|none||none|
|»» label_shipping|string|true|none||none|
|»» item_columns|string|true|none||none|
|»» footer_html|null|true|none||none|
|»» css_style|null|true|none||none|
|»» view_style|string|true|none||none|
|»» label_creditnote_no|string|true|none||none|
|»» label_creditnote_to|null|true|none||none|
|»» label_creditnote_date|string|true|none||none|
|»» label_estimate_no|string|true|none||none|
|»» label_estimate_date|string|true|none||none|
|»» refundreceipt_title|string|true|none||none|
|»» quantity_price|string|true|none||none|
|»» label_refundreceipt_no|string|true|none||none|
|»» label_refundreceipt_date|string|true|none||none|
|»» label_to|string|true|none||none|
|»» label_refunded|string|true|none||none|
|»» alt_template|integer|true|none||none|
|»» layout_type|integer|true|none||none|
|»» sticky_footer|string|true|none||none|
|»» sticky_header|string|true|none||none|
|»» default_purchase_refund|integer|true|none||none|
|»» default_purchase_order|integer|true|none||none|
|»» branch_id|integer|true|none||none|
|»» purchase_order_title|null|true|none||none|
|»» default_width|integer|true|none||none|
|»» default_height|integer|true|none||none|
|»» min_width|integer|true|none||none|
|»» min_height|integer|true|none||none|
|»» max_width|integer|true|none||none|
|»» max_height|integer|true|none||none|
|»» name|string|true|none||none|
|» invoice_installment_agreements|[string]|true|none||none|
|» invoice_requisitions|[string]|true|none||none|
|» journal_account_route|[string]|true|none||none|
|» invoice_appointments|[string]|true|none||none|
|» staff|null|true|none||none|
|» work_orders|null|true|none||none|
|» pos_shifts|null|true|none||none|
|» invoice_source_order|null|true|none||none|
|» custom_data|null|true|none||none|

## POST Add Advance Payment

POST /invoices

> Body Parameters

```json
{
    "Invoice": {
        "subscription_id": "",
        "store_id": 1,
        "type": 19,
        "po_number": 26,
        "client_id": 46,
        "client_email": "",
        "client_country_code": "SAR",
        "draft": "0",
        "follow_up_status": null,
        "staff_id": 0,
        "name": "",
        "is_offline": 1,
        "currency_code": "SAR",
        "payment_status": 2,
        "date": "2026-04-07",
        "discount": 0,
        "discount_amount": 0,
        "deposit": 0,
        "deposit_type": 0,
        "notes": "",
        "html_notes": "",
        "invoice_layout_id": 9,
        "estimate_id": 0,
        "shipping_options": "",
        "shipping_amount": null,
        "requisition_delivery_status": null,
        "pos_shift_id": null,
        "branch_id": 1
    },
    "Payment": {
        "client_id": null,
        "payment_method": "cash",
        "amount": 100,
        "transaction_id": "",
        "date": "2026-04-07 00:00:00",
        "email": null,
        "status": 1,
        "notes": null,
        "response_code": null,
        "response_message": null,
        "created": "2026-04-07 18:59:02",
        "currency_code": "SAR",
        "first_name": "",
        "last_name": "",
        "address1": null,
        "address2": "",
        "city": "",
        "state": "",
        "postal_code": "",
        "country_code": "",
        "phone1": "+966547895120",
        "phone2": null,
        "attachment": null,
        "staff_id": 4,
        "payment_work_order_id": null,
        "treasury_id": 1,
        "pos_shift_id": null,
        "receipt_notes": null,
        "extra_details": null,
        "branch_id": 1,
        "added_by": 1,
        "is_paid": 1
    },
    "InvoiceItem": [
        {
            "item": "خدمة",
            "description": "",
            "unit_price": 100,
            "quantity": 1,
            "col_3": "",
            "col_4": "",
            "tax1": 0,
            "tax2": 0,
            "product_id": 112
        }
    ],
    "InvoiceCustomField": []
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| yes |none|
|» Invoice|body|object| yes |none|
|»» subscription_id|body|string| yes |none|
|»» store_id|body|integer| yes |none|
|»» type|body|integer| yes |none|
|»» po_number|body|integer| yes |none|
|»» client_id|body|integer| yes |none|
|»» client_email|body|string| yes |none|
|»» client_country_code|body|string| yes |none|
|»» draft|body|string| yes |none|
|»» follow_up_status|body|null| yes |none|
|»» staff_id|body|integer| yes |none|
|»» name|body|string| yes |none|
|»» is_offline|body|integer| yes |none|
|»» currency_code|body|string| yes |none|
|»» payment_status|body|integer| yes |none|
|»» date|body|string| yes |none|
|»» discount|body|integer| yes |none|
|»» discount_amount|body|integer| yes |none|
|»» deposit|body|integer| yes |none|
|»» deposit_type|body|integer| yes |none|
|»» notes|body|string| yes |none|
|»» html_notes|body|string| yes |none|
|»» invoice_layout_id|body|integer| yes |none|
|»» estimate_id|body|integer| yes |none|
|»» shipping_options|body|string| yes |none|
|»» shipping_amount|body|null| yes |none|
|»» requisition_delivery_status|body|null| yes |none|
|»» pos_shift_id|body|null| yes |none|
|»» branch_id|body|integer| yes |none|
|» Payment|body|object| yes |none|
|»» client_id|body|null| yes |none|
|»» payment_method|body|string| yes |none|
|»» amount|body|integer| yes |none|
|»» transaction_id|body|string| yes |none|
|»» date|body|string| yes |none|
|»» email|body|null| yes |none|
|»» status|body|integer| yes |none|
|»» notes|body|null| yes |none|
|»» response_code|body|null| yes |none|
|»» response_message|body|null| yes |none|
|»» created|body|string| yes |none|
|»» currency_code|body|string| yes |none|
|»» first_name|body|string| yes |none|
|»» last_name|body|string| yes |none|
|»» address1|body|null| yes |none|
|»» address2|body|string| yes |none|
|»» city|body|string| yes |none|
|»» state|body|string| yes |none|
|»» postal_code|body|string| yes |none|
|»» country_code|body|string| yes |none|
|»» phone1|body|string| yes |none|
|»» phone2|body|null| yes |none|
|»» attachment|body|null| yes |none|
|»» staff_id|body|integer| yes |none|
|»» payment_work_order_id|body|null| yes |none|
|»» treasury_id|body|integer| yes |none|
|»» pos_shift_id|body|null| yes |none|
|»» receipt_notes|body|null| yes |none|
|»» extra_details|body|null| yes |none|
|»» branch_id|body|integer| yes |none|
|»» added_by|body|integer| yes |none|
|»» is_paid|body|integer| yes |none|
|» InvoiceItem|body|[object]| yes |none|
|»» item|body|string| no |none|
|»» description|body|string| no |none|
|»» unit_price|body|integer| no |none|
|»» quantity|body|integer| no |none|
|»» col_3|body|string| no |none|
|»» col_4|body|string| no |none|
|»» tax1|body|integer| no |none|
|»» tax2|body|integer| no |none|
|»» product_id|body|integer| no |none|
|» InvoiceCustomField|body|[string]| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v2 Endpoints/Using API v2

## GET Data Fetching — Filtered

GET /{entity}/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|entity|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

#### Enum

|Name|Value|
|---|---|
|entity|invoice|
|entity|estimate|
|entity|credit_note|
|entity|refund_receipt|
|entity|client|
|entity|supplier|
|entity|work_order|
|entity|follow_up_reminder|
|entity|invoice_payment|
|entity|product|
|entity|journal|
|entity|journal_account|
|entity|journal_cat|
|entity|expense|
|entity|tax|
|entity|purchase_refund|
|entity|store|
|entity|treasury|
|entity|product_category|
|entity|staff|
|entity|client_attendance_log|
|entity|follow_up_action|
|entity|follow_up_status|
|entity|purchase_order|
|entity|shift_day|
|entity|contract|
|entity|invoice_installment_agreement|
|entity|installment|
|entity|agreement_installment|
|entity|payslip|
|entity|invoice_item|
|entity|post|
|entity|product_bundle|
|entity|tracking_number|

> Response Examples

> 200 Response

```json
{
  "Responses": "string"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» Responses|string|true|none||none|

# API v2 Endpoints/Leave Application 

## GET Get All Leave Applications

GET /leave_application/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET Get Single Leave Applications 

GET /leave_application/{ID}/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|ID|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## PUT Edit Leave Application

PUT /leave_application/{ID}

> Body Parameters

```json
{
    "id": 10,
    "staff_id": "1",
    "days": "42",
    "date_from": "2025-11-18",
    "date_to": "2025-12-29",
    "type": "leave",
    "leave_type_id": "1",
    "late_time": "",
    "early_time": "",
    "description": "",
    "attachments": ""
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|ID|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## POST Add Leave Application

POST /leave_application

> Body Parameters

```json
{
    "id": "",
    "staff_id": "1",
    "days": "43",
    "date_from": "2025-11-17",
    "date_to": "2025-12-29",
    "type": "leave",
    "leave_type_id": "1",
    "late_time": "",
    "early_time": "",
    "description": "",
    "attachments": ""
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| yes |none|
|» id|body|string| yes |none|
|» staff_id|body|string| yes |none|
|» days|body|string| yes |none|
|» date_from|body|string| yes |none|
|» date_to|body|string| yes |none|
|» type|body|string| yes |none|
|» leave_type_id|body|string| yes |none|
|» late_time|body|string| yes |none|
|» early_time|body|string| yes |none|
|» description|body|string| yes |none|
|» attachments|body|string| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v2 Endpoints/Purchase Debit Note

## GET Purchase Debit Note

GET /v2/api/entity/purchase_debit_note/list/-1

> Body Parameters

```json
{
  "invoice_layout_id": 0,
  "type": "string",
  "supplier_id": 0,
  "currency_code": "string",
  "language_id": 0,
  "supplier_supplier_number": "string",
  "supplier_business_name": "string",
  "supplier_first_name": "string",
  "supplier_last_name": "string",
  "supplier_address1": "string",
  "supplier_address2": "string",
  "supplier_city": "string",
  "supplier_state": "string",
  "supplier_postal_code": "string",
  "supplier_phone1": "string",
  "supplier_phone2": "string",
  "supplier_country_code": "string",
  "supplier_bn1_label": "string",
  "supplier_bn2_label": "string",
  "supplier_default_currency_code": "string",
  "date": "string",
  "work_order_id": 0,
  "store_id": 0,
  "show_item_stores": "string",
  "shipping_tax_id": null,
  "shipping_amount": null,
  "discount": null,
  "discount_amount": null,
  "adjustment_label": "string",
  "adjustment_value": "string",
  "html_notes": null,
  "draft": "string",
  "purchase_order_item": [
    {
      "product_id": 0,
      "item": "string",
      "description": "string",
      "col_3": "string",
      "col_4": "string",
      "col_5": "string",
      "unit_price": 0,
      "quantity": 0,
      "discount": 0,
      "discount_type": 0,
      "tax1": null,
      "tax2": null
    }
  ],
  "summary_total": {
    "currency": "string"
  },
  "PurchaseOrderCustomField": {
    "0": {
      "label": "string",
      "value": "string"
    },
    "1": {
      "label": "string",
      "value": "string"
    },
    "2": {
      "label": "string",
      "value": "string"
    },
    "3": {
      "label": "string",
      "value": "string"
    },
    "4": {
      "label": "string",
      "value": "string"
    },
    "5": {
      "label": "string",
      "value": null
    }
  }
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|debug|query|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» invoice_layout_id|body|integer| yes |none|
|» type|body|string| yes |none|
|» supplier_id|body|integer| yes |none|
|» currency_code|body|string| yes |none|
|» language_id|body|integer| yes |none|
|» supplier_supplier_number|body|string| yes |none|
|» supplier_business_name|body|string| yes |none|
|» supplier_first_name|body|string| yes |none|
|» supplier_last_name|body|string| yes |none|
|» supplier_address1|body|string| yes |none|
|» supplier_address2|body|string| yes |none|
|» supplier_city|body|string| yes |none|
|» supplier_state|body|string| yes |none|
|» supplier_postal_code|body|string| yes |none|
|» supplier_phone1|body|string| yes |none|
|» supplier_phone2|body|string| yes |none|
|» supplier_country_code|body|string| yes |none|
|» supplier_bn1_label|body|string| yes |none|
|» supplier_bn2_label|body|string| yes |none|
|» supplier_default_currency_code|body|string| yes |none|
|» date|body|string| yes |none|
|» work_order_id|body|integer| yes |none|
|» store_id|body|integer| yes |none|
|» show_item_stores|body|string| yes |none|
|» shipping_tax_id|body|null| yes |none|
|» shipping_amount|body|null| yes |none|
|» discount|body|null| yes |none|
|» discount_amount|body|null| yes |none|
|» adjustment_label|body|string| yes |none|
|» adjustment_value|body|string| yes |none|
|» html_notes|body|null| yes |none|
|» draft|body|string| yes |none|
|» purchase_order_item|body|[object]| yes |none|
|»» product_id|body|integer| no |none|
|»» item|body|string| no |none|
|»» description|body|string| no |none|
|»» col_3|body|string| no |none|
|»» col_4|body|string| no |none|
|»» col_5|body|string| no |none|
|»» unit_price|body|integer| no |none|
|»» quantity|body|integer| no |none|
|»» discount|body|integer| no |none|
|»» discount_type|body|integer| no |none|
|»» tax1|body|null| no |none|
|»» tax2|body|null| no |none|
|» summary_total|body|object| yes |none|
|»» currency|body|string| yes |none|
|» PurchaseOrderCustomField|body|object| yes |none|
|»» 0|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 1|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 2|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 3|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 4|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 5|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|null| yes |none|

> Response Examples

> 200 Response

```json
{
  "message": "string",
  "id": 0
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

## POST Purchase Debit Note

POST /purchase_debit_note

> Body Parameters

```json
{
    "invoice_layout_id": 8,
    "type": "14",
    "supplier_id": 1,
    "currency_code": "EGP",
    "language_id": 7,
    "supplier_supplier_number": "000001",
    "supplier_business_name": "مورد",
    "supplier_first_name": "مورد",
    "supplier_last_name": "جديد",
    "supplier_address1": "22بب2",
    "supplier_address2": "3ي2",
    "supplier_city": "القرية",
    "supplier_state": "الذكية",
    "supplier_postal_code": "9999999",
    "supplier_phone1": "64646464646",
    "supplier_phone2": "6595959595",
    "supplier_country_code": "EG",
    "supplier_bn1_label": "سجل تجاري",
    "supplier_bn2_label": "بطاقة ضريبية",
    "supplier_default_currency_code": "EGP",
    "date": "23/03/2025",
    "work_order_id": 34,
    "store_id": 2,
    "show_item_stores": "0",
    "shipping_tax_id": null,
    "shipping_amount": null,
    "discount": null,
    "discount_amount": null,
    "adjustment_label": "",
    "adjustment_value": "",
    "html_notes": null,
    "draft": "1",
       "purchase_debit_notes_items": [
        {
 
            "product_id": 2,
            "item": "منتج 1",
            "description": "",
            "col_3": "",
            "col_4": "",
            "col_5": "",
            "unit_price": 100,
            "quantity": 1,
            "discount": 0,
            "discount_type": 1,
            "tax1": null,
            "tax2": null
    }
    ],
    "summary_total": {
        "currency": "EGP"
    },
    "PurchaseOrderCustomField": {
        "0": {
            "label": "الإجمالي",
            "value": "%total%"
        },
        "1": {
            "label": "القيمة المضافة",
            "value": "10"
        },
        "2": {
            "label": "الأجمالى",
            "value": "5"
        },
        "3": {
            "label": "المدفوع",
            "value": "8"
        },
        "4": {
            "label": "الرصيد المستحق",
            "value": "9"
        },
        "5": {
            "label": "PO NO",
            "value": null
        }
    }

}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|apikey|header|string| no |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|body|body|object| no |none|
|» invoice_layout_id|body|integer| yes |none|
|» type|body|string| yes |none|
|» supplier_id|body|integer| yes |none|
|» currency_code|body|string| yes |none|
|» language_id|body|integer| yes |none|
|» supplier_supplier_number|body|string| yes |none|
|» supplier_business_name|body|string| yes |none|
|» supplier_first_name|body|string| yes |none|
|» supplier_last_name|body|string| yes |none|
|» supplier_address1|body|string| yes |none|
|» supplier_address2|body|string| yes |none|
|» supplier_city|body|string| yes |none|
|» supplier_state|body|string| yes |none|
|» supplier_postal_code|body|string| yes |none|
|» supplier_phone1|body|string| yes |none|
|» supplier_phone2|body|string| yes |none|
|» supplier_country_code|body|string| yes |none|
|» supplier_bn1_label|body|string| yes |none|
|» supplier_bn2_label|body|string| yes |none|
|» supplier_default_currency_code|body|string| yes |none|
|» date|body|string| yes |none|
|» work_order_id|body|integer| yes |none|
|» store_id|body|integer| yes |none|
|» show_item_stores|body|string| yes |none|
|» shipping_tax_id|body|null| yes |none|
|» shipping_amount|body|null| yes |none|
|» discount|body|null| yes |none|
|» discount_amount|body|null| yes |none|
|» adjustment_label|body|string| yes |none|
|» adjustment_value|body|string| yes |none|
|» html_notes|body|null| yes |none|
|» draft|body|string| yes |none|
|» purchase_order_item|body|[object]| yes |none|
|»» product_id|body|integer| no |none|
|»» item|body|string| no |none|
|»» description|body|string| no |none|
|»» col_3|body|string| no |none|
|»» col_4|body|string| no |none|
|»» col_5|body|string| no |none|
|»» unit_price|body|integer| no |none|
|»» quantity|body|integer| no |none|
|»» discount|body|integer| no |none|
|»» discount_type|body|integer| no |none|
|»» tax1|body|null| no |none|
|»» tax2|body|null| no |none|
|» summary_total|body|object| yes |none|
|»» currency|body|string| yes |none|
|» PurchaseOrderCustomField|body|object| yes |none|
|»» 0|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 1|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 2|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 3|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 4|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|string| yes |none|
|»» 5|body|object| yes |none|
|»»» label|body|string| yes |none|
|»»» value|body|null| yes |none|

> Response Examples

> 200 Response

```json
{
  "message": "string",
  "id": 0
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

# API v2 Endpoints/Branches 

## GET Get All Branches 

GET /branches

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "result": "string",
  "code": 0,
  "data": [
    {
      "Branch": {
        "id": "string",
        "code": "string",
        "name": "string",
        "phone1": "string",
        "phone2": "string",
        "working_hours": "string",
        "description": "string",
        "address1": "string",
        "address2": "string",
        "city": "string",
        "state": "string",
        "country_code": "string",
        "admin_staff_id": "string",
        "staff_id": "string",
        "smtp_account_id": "string",
        "status": "string",
        "map_location": null,
        "created": "string",
        "modified": "string"
      }
    }
  ],
  "pagination": {
    "prev": null,
    "next": null,
    "page": 0,
    "page_count": 0,
    "total_results": 0
  }
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|true|none||none|
|» code|integer|true|none||none|
|» data|[object]|true|none||none|
|»» Branch|object|false|none||none|
|»»» id|string|true|none||none|
|»»» code|string|true|none||none|
|»»» name|string|true|none||none|
|»»» phone1|string|true|none||none|
|»»» phone2|string|true|none||none|
|»»» working_hours|string|true|none||none|
|»»» description|string|true|none||none|
|»»» address1|string|true|none||none|
|»»» address2|string|true|none||none|
|»»» city|string|true|none||none|
|»»» state|string|true|none||none|
|»»» country_code|string|true|none||none|
|»»» admin_staff_id|string|true|none||none|
|»»» staff_id|string|true|none||none|
|»»» smtp_account_id|string|true|none||none|
|»»» status|string|true|none||none|
|»»» map_location|null|true|none||none|
|»»» created|string|true|none||none|
|»»» modified|string|true|none||none|
|» pagination|object|true|none||none|
|»» prev|null|true|none||none|
|»» next|null|true|none||none|
|»» page|integer|true|none||none|
|»» page_count|integer|true|none||none|
|»» total_results|integer|true|none||none|

# API v2 Endpoints/Product Bundles

## POST Add Product bundle

POST /product_bundle

> Body Parameters

```json
{
    "product_id": "id of the item you want to assign to the bundle ",
    "bundle_product_id": "id of the bundle product",
    "quantity": 2,
    "unit_name": null,
    "unit_factor": null,
    "unit_small_name": null,
    "unit_factor_id": null
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v2 Endpoints/Follow Up Statuses

## GET GET All Follow Up Statuses

GET /follow_up_statuses/{type}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|type|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    null
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[any]|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Follow Up Status

GET /follow_up_statuses/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": null,
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Follow Up Status

DELETE /follow_up_statuses/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v2 Endpoints/Follow Up Actions

## GET GET All Follow Up Actions

GET /follow_up_actions/{type}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|type|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": [
    null
  ],
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|[any]|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## GET GET Single Follow Up Action

GET /follow_up_actions/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": null,
  "pagination": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|any|false|none||none|
|» pagination|any|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

## DELETE Delete Follow Up Action

DELETE /follow_up_actions/{id}{format}

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful"
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Item can't be deleted, check the the transactions of the item|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|NotFound|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|

HTTP Status Code **400**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **404**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **500**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# API v2 Endpoints/Attendance Logs

## GET Get All Attendance Logs

GET /attendance_log/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET Get Single Attendance Log

GET /attendance_log/{id}/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|id|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## POST Add Attendance Log

POST /attendance_log

> Body Parameters

```json
{
  "session_id": 2,
  "source_id": 4,
  "source_method": null,
  "source_name": "Staff Name",
  "source_type": "supervisor",
  "staff_id": 2,
  "status": "draft",
  "time": "2025-10-01 07:51:00"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| yes |none|
|» session_id|body|integer| yes |none|
|» source_id|body|integer| yes |none|
|» source_method|body|null| yes |none|
|» source_name|body|string| yes |none|
|» source_type|body|string| yes |none|
|» staff_id|body|integer| yes |none|
|» status|body|string| yes |Should be draft|
|» time|body|string| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v2 Endpoints/Cost Centers

## GET GET All Cost Centers

GET /cost_center/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET GET Single Cost Center

GET /cost_center/{ID}/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|ID|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## PUT Edit Cost Center

PUT /v2/api/entity/cost_center/{ID}

> Body Parameters

```json
{
    "id": 37,
    "name":  "Cost center name",
    "code": 36,
    "is_primary": 1,
    "cost_center_id": 0,
    "cost_center_ids": "0",
    "branch_id": 1
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|ID|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## POST Add New Cost Center

POST /v2/api/entity/cost_center

> Body Parameters

```json
{
    "name": "Project D",
    "code": "0001",
    "is_primary": "0",
    "cost_center_id": 5,
    "cost_center_ids": "5",
    "branch_id": 1
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| yes |none|
|» name|body|string| yes |none|
|» code|body|string| yes |code is unique|
|» is_primary|body|string| yes |1 for primary cost center|
|» cost_center_id|body|integer| yes |parent id and "0" for primary|
|» cost_center_ids|body|string| yes |none|
|» branch_id|body|integer| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v2 Endpoints/Payment Gateways

## GET Get All Payment Methods

GET /site_payment_gateway/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## GET Get Single Payment Method

GET /site_payment_gateway/{ID}/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|ID|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

## POST Add Payment Method

POST /site_payment_gateway

> Body Parameters

```json
{
"id": 27,
"payment_gateway": "newpaymentmethod",
"label": "نقدى جديد ",
"username": null,
"option1": "",
"option2": null,
"option3": null,
"default": 0,
"active": 1,
"manually_added": 1,
"disable_for_client": 0,
"settings": null,
"treasury_id": null,
"branch_id": 1

}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| yes |none|
|» id|body|integer| yes |none|
|» payment_gateway|body|string| yes |none|
|» label|body|string| yes |none|
|» username|body|null| yes |none|
|» option1|body|string| yes |none|
|» option2|body|null| yes |none|
|» option3|body|null| yes |none|
|» default|body|integer| yes |none|
|» active|body|integer| yes |none|
|» manually_added|body|integer| yes |none|
|» disable_for_client|body|integer| yes |none|
|» settings|body|null| yes |none|
|» treasury_id|body|null| yes |none|
|» branch_id|body|integer| yes |none|

> Response Examples

> 200 Response

```json
{}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### Responses Data Schema

# API v2 Endpoints/Points & Credits/Credit Usage

## GET Get All Credit Usage

GET /credit_usage/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "current_page": 1,
    "data": [
        {
            "id": 12,
            "client_id": 13,
            "credit_type_id": 1,
            "usage_date": "2026-10-20",
            "description": "Test Description",
            "created": "2026-02-10 12:42:20",
            "modified": "2026-02-10 12:42:20",
            "deleted_at": null
        },
        {
            "id": 11,
            "client_id": 12,
            "credit_type_id": 1,
            "usage_date": "2026-02-28",
            "description": null,
            "created": "2026-01-15 12:35:32",
            "modified": "2026-01-15 12:35:32",
            "deleted_at": null
        }
    ],
    "first_page_url": "/v2/api/entity/credit_usage/list/1?page=1",
    "from": 1,
    "last_page": 6,
    "last_page_url": "/v2/api/entity/credit_usage/list/1?page=6",
    "links": [
        {
            "url": null,
            "label": "pagination.previous",
            "page": null,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_usage/list/1?page=1",
            "label": "1",
            "page": 1,
            "active": true
        },
        {
            "url": "/v2/api/entity/credit_usage/list/1?page=2",
            "label": "2",
            "page": 2,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_usage/list/1?page=3",
            "label": "3",
            "page": 3,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_usage/list/1?page=4",
            "label": "4",
            "page": 4,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_usage/list/1?page=5",
            "label": "5",
            "page": 5,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_usage/list/1?page=6",
            "label": "6",
            "page": 6,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_usage/list/1?page=2",
            "label": "pagination.next",
            "page": 2,
            "active": false
        }
    ],
    "next_page_url": "/v2/api/entity/credit_usage/list/1?page=2",
    "path": "/v2/api/entity/credit_usage/list/1",
    "per_page": 2,
    "prev_page_url": null,
    "to": 2,
    "total": 12
}
```

> 401 Response

```json
{
  "message": null
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» current_page|integer|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||none|
|»» client_id|integer|true|none||none|
|»» credit_type_id|integer|true|none||none|
|»» usage_date|string|true|none||none|
|»» description|string¦null|true|none||none|
|»» created|string|true|none||none|
|»» modified|string|true|none||none|
|»» deleted_at|null|true|none||none|
|» first_page_url|string|true|none||none|
|» from|integer|true|none||none|
|» last_page|integer|true|none||none|
|» last_page_url|string|true|none||none|
|» links|[object]|true|none||none|
|»» url|string¦null|true|none||none|
|»» label|string|true|none||none|
|»» page|integer¦null|true|none||none|
|»» active|boolean|true|none||none|
|» next_page_url|string|true|none||none|
|» path|string|true|none||none|
|» per_page|integer|true|none||none|
|» prev_page_url|null|true|none||none|
|» to|integer|true|none||none|
|» total|integer|true|none||none|
|» code|integer|true|none||none|
|» result|string|true|none||none|
|» pagination|object|true|none||none|
|»» prev|string|true|none||none|
|»» next|string|true|none||none|
|»» page|integer|true|none||none|
|»» page_count|integer|true|none||none|
|»» total_results|integer|true|none||none|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|any|true|none||none|

## GET Get Single Credit Usage 

GET /credit_usage/id/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "id": 10,
    "client_id": 13,
    "credit_type_id": 1,
    "usage_date": "2025-10-31",
    "description": "Test Amount",
    "created": "2026-01-01 13:27:17",
    "modified": "2026-01-01 13:27:17",
    "deleted_at": null
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» client_id|integer|true|none||none|
|» credit_type_id|integer|true|none||none|
|» usage_date|string|true|none||none|
|» description|string|true|none||none|
|» created|string|true|none||none|
|» modified|string|true|none||none|
|» deleted_at|null|true|none||none|

## POST Edit Credit Usage

POST /credit_usage

> Body Parameters

```json
{
    "id": 5,
    "client_id": 13,
    "credit_type_id": "1",
    "description": "Test Description"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» id|body|integer| yes |none|
|» client_id|body|integer| yes |none|
|» credit_type_id|body|string| yes |none|
|» description|body|string| yes |none|
|» amount|body|integer| yes |none|

> Response Examples

> 200 Response

```json
{
    "message": "Credit Usage Added Successfully",
    "id": 16
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

## POST Edit Credit Usage Amount

POST /charge_usage

> Body Parameters

```json
{
    "id": 5,
    "credit_charge_id": "216",
    "credit_usage_id": "11",
    "amount": 300
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» id|body|integer| yes |none|
|» credit_charge_id|body|string| yes |none|
|» credit_usage_id|body|string| yes |none|
|» amount|body|integer| yes |none|

> Response Examples

> 200 Response

```json
{
    "message": "Charge Usage Added Successfully",
    "id": 5
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

## GET Get All Credit Usage Amount

GET /charge_usage/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "current_page": 1,
    "data": [
        {
            "id": 7,
            "credit_charge_id": 216,
            "credit_usage_id": 11,
            "amount": 300
        },
        {
            "id": 6,
            "credit_charge_id": 216,
            "credit_usage_id": 11,
            "amount": 300
        },
        {
            "id": 5,
            "credit_charge_id": 216,
            "credit_usage_id": 11,
            "amount": 300
        },
        {
            "id": 4,
            "credit_charge_id": 1,
            "credit_usage_id": 5,
            "amount": 11
        },
        {
            "id": 3,
            "credit_charge_id": 3,
            "credit_usage_id": 4,
            "amount": 31
        },
        {
            "id": 2,
            "credit_charge_id": 2,
            "credit_usage_id": 4,
            "amount": 8
        },
        {
            "id": 1,
            "credit_charge_id": 2,
            "credit_usage_id": 1,
            "amount": 20
        }
    ],
    "first_page_url": "/v2/api/entity/charge_usage/list/1?page=1",
    "from": 1,
    "last_page": 1,
    "last_page_url": "/v2/api/entity/charge_usage/list/1?page=1",
    "links": [
        {
            "url": null,
            "label": "pagination.previous",
            "page": null,
            "active": false
        },
        {
            "url": "/v2/api/entity/charge_usage/list/1?page=1",
            "label": "1",
            "page": 1,
            "active": true
        },
        {
            "url": null,
            "label": "pagination.next",
            "page": null,
            "active": false
        }
    ],
    "next_page_url": null,
    "path": "/v2/api/entity/charge_usage/list/1",
    "per_page": 20,
    "prev_page_url": null,
    "to": 7,
    "total": 7
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» current_page|integer|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||none|
|»» credit_charge_id|integer|true|none||none|
|»» credit_usage_id|integer|true|none||none|
|»» amount|integer|true|none||none|
|» first_page_url|string|true|none||none|
|» from|integer|true|none||none|
|» last_page|integer|true|none||none|
|» last_page_url|string|true|none||none|
|» links|[object]|true|none||none|
|»» url|string¦null|true|none||none|
|»» label|string|true|none||none|
|»» page|integer¦null|true|none||none|
|»» active|boolean|true|none||none|
|» next_page_url|null|true|none||none|
|» path|string|true|none||none|
|» per_page|integer|true|none||none|
|» prev_page_url|null|true|none||none|
|» to|integer|true|none||none|
|» total|integer|true|none||none|

## GET Get Single Credit Usage Amount

GET /charge_usage/id/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "id": 1,
    "credit_charge_id": 2,
    "credit_usage_id": 1,
    "amount": 20
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» credit_charge_id|integer|true|none||none|
|» credit_usage_id|integer|true|none||none|
|» amount|integer|true|none||none|

# API v2 Endpoints/Points & Credits/Credit Types

## GET Get All Credit types

GET /credit_type/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "current_page": 1,
    "data": [
        {
            "id": 8,
            "name": "Test credit 4",
            "allow_decimal": 1,
            "status": 1,
            "unit": "نقطة",
            "description": "Hello",
            "created": "2026-01-01 13:16:04",
            "modified": "2026-01-01 13:16:04",
            "deleted_at": null
        },
        {
            "id": 4,
            "name": "Test credit",
            "allow_decimal": 0,
            "status": 1,
            "unit": null,
            "description": null,
            "created": "2025-12-27 22:39:15",
            "modified": "2025-12-27 22:39:15",
            "deleted_at": null
        },
        {
            "id": 3,
            "name": "Test 1",
            "allow_decimal": 0,
            "status": 1,
            "unit": null,
            "description": null,
            "created": "2025-12-28 00:38:48",
            "modified": "2025-12-28 00:38:48",
            "deleted_at": null
        }
    ],
    "first_page_url": "/v2/api/entity/credit_type/list/1?page=1",
    "from": 1,
    "last_page": 1,
    "last_page_url": "/v2/api/entity/credit_type/list/1?page=1",
    "links": [
        {
            "url": null,
            "label": "pagination.previous",
            "page": null,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_type/list/1?page=1",
            "label": "1",
            "page": 1,
            "active": true
        },
        {
            "url": null,
            "label": "pagination.next",
            "page": null,
            "active": false
        }
    ],
    "next_page_url": null,
    "path": "/v2/api/entity/credit_type/list/1",
    "per_page": 20,
    "prev_page_url": null,
    "to": 8,
    "total": 8
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» current_page|integer|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||none|
|»» name|string|true|none||none|
|»» allow_decimal|integer|true|none||none|
|»» status|integer|true|none||none|
|»» unit|string¦null|true|none||none|
|»» description|string¦null|true|none||none|
|»» created|string|true|none||none|
|»» modified|string|true|none||none|
|»» deleted_at|null|true|none||none|
|» first_page_url|string|true|none||none|
|» from|integer|true|none||none|
|» last_page|integer|true|none||none|
|» last_page_url|string|true|none||none|
|» links|[object]|true|none||none|
|»» url|string¦null|true|none||none|
|»» label|string|true|none||none|
|»» page|integer¦null|true|none||none|
|»» active|boolean|true|none||none|
|» next_page_url|null|true|none||none|
|» path|string|true|none||none|
|» per_page|integer|true|none||none|
|» prev_page_url|null|true|none||none|
|» to|integer|true|none||none|
|» total|integer|true|none||none|

## GET Get Single Credit type 

GET /credit_type/id/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "id": 8,
    "name": "Test credit 4",
    "allow_decimal": 1,
    "status": 1,
    "unit": "نقطة",
    "description": "Hello",
    "created": "2026-01-01 13:16:04",
    "modified": "2026-01-01 13:16:04",
    "deleted_at": null
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» name|string|true|none||none|
|» allow_decimal|integer|true|none||none|
|» status|integer|true|none||none|
|» unit|string|true|none||none|
|» description|string|true|none||none|
|» created|string|true|none||none|
|» modified|string|true|none||none|
|» deleted_at|null|true|none||none|

## POST Edit Credit type

POST /credit_type

> Body Parameters

```json
{
    "id": 7,
    "name": "Test credit 4 edited",
    "allow_decimal": 0,
    "status": 1,
    "unit": "نقطة",
    "description": "Test Description"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» id|body|integer| yes |none|
|» name|body|string| yes |none|
|» allow_decimal|body|integer| yes |none|
|» status|body|integer| yes |1 --> Active|
|» unit|body|string| yes |none|
|» description|body|string| yes |none|

#### Description

**» status**: 1 --> Active
 0 --> Inactive

> Response Examples

> 200 Response

```json
{
    "message": "Credit Type Added Successfully",
    "id": 7
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

# API v2 Endpoints/Points & Credits/Credit Charges

## GET Get All Credit Charges

GET /credit_charge/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
  "current_page": 1,
  "data": [
    {
      "id": 277,
      "staff_id": 1,
      "client_id": 1,
      "credit_type_id": 1,
      "status": "available",
      "start_date": "2026-02-12",
      "expiry_date": null,
      "amount": 1.25,
      "description": "تم الحصول على 1.25 نقاط الولاء لشراء فى دفع 25.00 ج.م فى فاتورة #*DSR2602467",
      "created": "2026-02-12 15:39:58",
      "modified": "2026-02-12 15:39:58",
      "deleted_at": null,
      "renewal_id": null
    }
  ],
  "first_page_url": "/v2/api/entity/credit_charge/list/1?page=1",
  "from": 1,
  "last_page": 14,
  "last_page_url": "/v2/api/entity/credit_charge/list/1?page=14",
  "links": [
    {
      "url": null,
      "label": "pagination.previous",
      "page": null,
      "active": false
    },
    {
      "url": "/v2/api/entity/credit_charge/list/1?page=1",
      "label": "1",
      "page": 1,
      "active": true
    }
  ],
  "next_page_url": "/v2/api/entity/credit_charge/list/1?page=2",
  "path": "/v2/api/entity/credit_charge/list/1",
  "per_page": 20,
  "prev_page_url": null,
  "to": 20,
  "total": 276
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» current_page|integer|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|false|none||none|
|»» staff_id|integer|false|none||none|
|»» client_id|integer|false|none||none|
|»» credit_type_id|integer|false|none||none|
|»» status|string|false|none||none|
|»» start_date|string|false|none||none|
|»» expiry_date|null|false|none||none|
|»» amount|number|false|none||none|
|»» description|string|false|none||none|
|»» created|string|false|none||none|
|»» modified|string|false|none||none|
|»» deleted_at|null|false|none||none|
|»» renewal_id|null|false|none||none|
|» first_page_url|string|true|none||none|
|» from|integer|true|none||none|
|» last_page|integer|true|none||none|
|» last_page_url|string|true|none||none|
|» links|[object]|true|none||none|
|»» url|string¦null|true|none||none|
|»» label|string|true|none||none|
|»» page|integer¦null|true|none||none|
|»» active|boolean|true|none||none|
|» next_page_url|string|true|none||none|
|» path|string|true|none||none|
|» per_page|integer|true|none||none|
|» prev_page_url|null|true|none||none|
|» to|integer|true|none||none|
|» total|integer|true|none||none|

## GET Get Single Credit Charge

GET /credit_charge/id/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "id": 277,
    "staff_id": 1,
    "client_id": 1,
    "credit_type_id": 1,
    "status": "available",
    "start_date": "2026-02-12",
    "expiry_date": null,
    "amount": 1.25,
    "description": "تم الحصول على 1.25 نقاط الولاء لشراء فى دفع 25.00 ج.م فى فاتورة #*DSR2602467",
    "created": "2026-02-12 15:39:58",
    "modified": "2026-02-12 15:39:58",
    "deleted_at": null,
    "renewal_id": null
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» staff_id|integer|true|none||none|
|» client_id|integer|true|none||none|
|» credit_type_id|integer|true|none||none|
|» status|string|true|none||none|
|» start_date|string|true|none||none|
|» expiry_date|null|true|none||none|
|» amount|number|true|none||none|
|» description|string|true|none||none|
|» created|string|true|none||none|
|» modified|string|true|none||none|
|» deleted_at|null|true|none||none|
|» renewal_id|null|true|none||none|

## POST Edit Credit Charge

POST /credit_charge

> Body Parameters

```json
{
    "id": 221,
    "staff_id": 1,
    "client_id": 1,
    "credit_type_id": "2",
    "start_date": "31/12/2025",
    "expiry_date": "31/12/2025",
    "amount": 200,
    "description": "Test Description"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» id|body|integer| yes |none|
|» staff_id|body|integer| yes |none|
|» client_id|body|integer| yes |none|
|» credit_type_id|body|string| yes |none|
|» start_date|body|string| yes |none|
|» expiry_date|body|string| yes |none|
|» amount|body|integer| yes |none|
|» description|body|string| yes |none|

> Response Examples

> 200 Response

```json
{
    "message": "Credit Charge Added Successfully",
    "id": 221
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

# API v2 Endpoints/Points & Credits/Packages

## GET Get All Packages

GET /package/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|per_page|query|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "current_page": 1,
    "data": [
        {
            "id": 34,
            "name": "Package Test 4.3",
            "price": 350,
            "period_value": 1,
            "period_unit": "monthly",
            "status": 1,
            "product_id": null,
            "description": "Test Description 2.0",
            "created": "2026-02-10 13:04:49",
            "modified": "2026-02-10 13:04:49",
            "deleted_at": null,
            "type": "membership",
            "branch_id": 1
        },
        {
            "id": 33,
            "name": "Package Test 4.3",
            "price": 250,
            "period_value": 1,
            "period_unit": "monthly",
            "status": 1,
            "product_id": null,
            "description": null,
            "created": "2026-01-01 08:26:31",
            "modified": "2026-01-01 08:26:31",
            "deleted_at": null,
            "type": "membership",
            "branch_id": 1
        }
    ],
    "first_page_url": "/v2/api/entity/package/list/1?page=1",
    "from": 1,
    "last_page": 1,
    "last_page_url": "/v2/api/entity/package/list/1?page=1",
    "links": [
        {
            "url": null,
            "label": "pagination.previous",
            "page": null,
            "active": false
        },
        {
            "url": "/v2/api/entity/package/list/1?page=1",
            "label": "1",
            "page": 1,
            "active": true
        },
        {
            "url": null,
            "label": "pagination.next",
            "page": null,
            "active": false
        }
    ],
    "next_page_url": null,
    "path": "/v2/api/entity/package/list/1",
    "per_page": 100,
    "prev_page_url": null,
    "to": 5,
    "total": 5
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» current_page|integer|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||none|
|»» name|string|true|none||none|
|»» price|integer|true|none||none|
|»» period_value|integer|true|none||none|
|»» period_unit|string|true|none||none|
|»» status|integer|true|none||none|
|»» product_id|null|true|none||none|
|»» description|string¦null|true|none||none|
|»» created|string|true|none||none|
|»» modified|string|true|none||none|
|»» deleted_at|null|true|none||none|
|»» type|string|true|none||none|
|»» branch_id|integer|true|none||none|
|» first_page_url|string|true|none||none|
|» from|integer|true|none||none|
|» last_page|integer|true|none||none|
|» last_page_url|string|true|none||none|
|» links|[object]|true|none||none|
|»» url|string¦null|true|none||none|
|»» label|string|true|none||none|
|»» page|integer¦null|true|none||none|
|»» active|boolean|true|none||none|
|» next_page_url|null|true|none||none|
|» path|string|true|none||none|
|» per_page|integer|true|none||none|
|» prev_page_url|null|true|none||none|
|» to|integer|true|none||none|
|» total|integer|true|none||none|

## GET Get Single Package

GET /package/id/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|per_page|query|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "id": 34,
    "name": "Package Test 4.3",
    "price": 350,
    "period_value": 1,
    "period_unit": "monthly",
    "status": 1,
    "product_id": null,
    "description": "Test Description 2.0",
    "created": "2026-02-10 13:04:49",
    "modified": "2026-02-10 13:04:49",
    "deleted_at": null,
    "type": "membership",
    "branch_id": 1
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» name|string|true|none||none|
|» price|integer|true|none||none|
|» period_value|integer|true|none||none|
|» period_unit|string|true|none||none|
|» status|integer|true|none||none|
|» product_id|null|true|none||none|
|» description|string|true|none||none|
|» created|string|true|none||none|
|» modified|string|true|none||none|
|» deleted_at|null|true|none||none|
|» type|string|true|none||none|
|» branch_id|integer|true|none||none|

## POST Edit Package

POST /package

> Body Parameters

```json
{
    "id": 30,
    "name": "Test Package 2.0 edited",
    "status": 1,
    "type": "membership", 
    "price": 100,
    "period_value": 1,
    "period_unit": "monthly", 
    "description": "Test Description"
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» id|body|integer| yes |none|
|» name|body|string| yes |none|
|» status|body|integer| yes |none|
|» type|body|string| yes |"credit_charge" | "membership"|
|» price|body|integer| yes |none|
|» period_value|body|integer| yes |none|
|» period_unit|body|string| yes |"daily" | "weekly" | "monthly" | "yearly"|
|» description|body|string| yes |none|

> Response Examples

> 200 Response

```json
{
    "message": "Package Added Successfully",
    "id": 30
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

# API v2 Endpoints/Points & Credits/Packages Credit Types

## GET Get All Package Credit Types

GET /credit_type_package/list/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "current_page": 1,
    "data": [
        {
            "id": 10,
            "credit_type_id": 1,
            "package_id": 24,
            "amount": 3500
        },
        {
            "id": 9,
            "credit_type_id": 1,
            "package_id": 24,
            "amount": 1000
        },
        {
            "id": 6,
            "credit_type_id": 2,
            "package_id": 33,
            "amount": 60
        }
    ],
    "first_page_url": "/v2/api/entity/credit_type_package/list?page=1",
    "from": 1,
    "last_page": 1,
    "last_page_url": "/v2/api/entity/credit_type_package/list?page=1",
    "links": [
        {
            "url": null,
            "label": "pagination.previous",
            "page": null,
            "active": false
        },
        {
            "url": "/v2/api/entity/credit_type_package/list?page=1",
            "label": "1",
            "page": 1,
            "active": true
        },
        {
            "url": null,
            "label": "pagination.next",
            "page": null,
            "active": false
        }
    ],
    "next_page_url": null,
    "path": "/v2/api/entity/credit_type_package/list",
    "per_page": 20,
    "prev_page_url": null,
    "to": 8,
    "total": 8
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» current_page|integer|true|none||none|
|» data|[object]|true|none||none|
|»» id|integer|true|none||none|
|»» credit_type_id|integer|true|none||none|
|»» package_id|integer|true|none||none|
|»» amount|integer|true|none||none|
|» first_page_url|string|true|none||none|
|» from|integer|true|none||none|
|» last_page|integer|true|none||none|
|» last_page_url|string|true|none||none|
|» links|[object]|true|none||none|
|»» url|string¦null|true|none||none|
|»» label|string|true|none||none|
|»» page|integer¦null|true|none||none|
|»» active|boolean|true|none||none|
|» next_page_url|null|true|none||none|
|» path|string|true|none||none|
|» per_page|integer|true|none||none|
|» prev_page_url|null|true|none||none|
|» to|integer|true|none||none|
|» total|integer|true|none||none|

## GET Get Single Package Credit Type

GET /credit_type_package/id/1

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|

> Response Examples

> 200 Response

```json
{
    "id": 10,
    "credit_type_id": 1,
    "package_id": 24,
    "amount": 3500
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» id|integer|true|none||none|
|» credit_type_id|integer|true|none||none|
|» package_id|integer|true|none||none|
|» amount|integer|true|none||none|

## POST Edit Package Credit Type

POST /credit_type_package

> Body Parameters

```json
{
    "id": 1,
    "credit_type_id": 1,
    "package_id": 24,
    "amount": 1000
}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|
|» id|body|integer| yes |none|
|» credit_type_id|body|integer| yes |none|
|» package_id|body|integer| yes |none|
|» amount|body|integer| yes |none|

> Response Examples

> 200 Response

```json
{
    "message": "Credit Type Package Added Successfully",
    "id": 1
}
```

> 401 Response

```json
null
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|none|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» message|string|true|none||none|
|» id|integer|true|none||none|

# API v2 Endpoints/Site

## GET GET Site Info

GET /site_info{format}

Get current site info

> Body Parameters

```json
{}
```

### Params

|Name|Location|Type|Required|Description|
|---|---|---|---|---|
|format|path|string| yes |none|
|Accept|header|string| no |none|
|Content-Type|header|string| no |none|
|Authorization|header|string| no |You can generate the bearer token using the the authorization endpoint then use it here to be able to operate over your account's data|
|apikey|header|string| no |You can find/generate your apikey(s) from inside your Daftra Account|
|body|body|object| no |none|

> Response Examples

> 200 Response

```json
{
  "code": 200,
  "result": "successful",
  "data": {
    "Site": {
      "id": 44,
      "business_name": "Communication Techniques for",
      "first_name": "ERNBKB",
      "last_name": "Team",
      "subdomain": "hrizam.daftara.com",
      "site_logo": "5a5b5b9c3b59c_5964b28344347_genie3.png",
      "invoice_logo": null,
      "address1": "abozabal",
      "address2": "hhy",
      "city": "khanka",
      "state": "qlyuopia",
      "postal_code": "13758",
      "phone1": "1022415830",
      "phone2": "1022415830",
      "country_code": "SA",
      "timezone": "13",
      "date_format": "3",
      "currency_code": "USD",
      "language_code": 41,
      "email": "example@example.com",
      "staff_id": -1,
      "currencyFormat": "$%s",
      "numberFormat": [
        2,
        ".",
        ","
      ],
      "SITE_HASH": "db4715bd"
    }
  }
}
```

### Responses

|HTTP Status Code |Meaning|Description|Data schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized|Inline|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|Inline|

### Responses Data Schema

HTTP Status Code **200**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» code|integer|false|none||none|
|» result|string|false|none||none|
|» data|object|false|none||none|
|»» Site|object|false|none||none|
|»»» id|integer(int32)|false|none||current site id|
|»»» business_name|string|false|none||business name of the owner|
|»»» first_name|string|false|none||First name of the owner|
|»»» last_name|string|false|none||Last name of the owner|
|»»» subdomain|string|false|none||subdomin of the site|
|»»» site_logo|string|false|none||default site logo|
|»»» invoice_logo|string|false|none||default invoice logo|
|»»» address1|string|false|none||address1 of the owner|
|»»» address2|string|false|none||address2 of the owner|
|»»» city|string|false|none||city of the owner|
|»»» state|string|false|none||state of the owner|
|»»» postal_code|string|false|none||postal code of the owner|
|»»» phone1|string|false|none||phone1 of the owner|
|»»» phone2|string|false|none||phone2 of the owner|
|»»» country_code|string|false|none||countey code of the owner|
|»»» timezone|integer|false|none||timezone of the owner [GET General Listing API with model `Timezone`](/15115384e0)|
|»»» date_format|integer|false|none||date format of the site [GET General Listing API with model `dateFormats`](/15115384e0)|
|»»» currency_code|string|false|none||default currency code|
|»»» language_code|string|false|none||default language code|
|»»» email|string(email)|false|none||owner email|
|»»» staff_id|integer|false|none||current staff id ```Equals -1 if access the api from different domain via ``` [APIKEY](#section/Authentication/APIKEY) get it from [GET STAFF](/15115376e0)|
|»»» is_super_admin|boolean¦null|false|none||if the current staff is super admin ```note that if the current staff is not super admin this parameter is not returned```|
|»»» currencyFormat|string|false|none||default currency format|
|»»» numberFormat|[string]|false|none||Array of three indcies that specify default number format `0 => how many decimals` `1 => decimalpoint symbol` `2 => separator symbol`|
|»»» SITE_HASH|string|false|none||current site hash|

HTTP Status Code **401**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

HTTP Status Code **403**

|Name|Type|Required|Restrictions|Title|description|
|---|---|---|---|---|---|
|» result|string|false|none||none|
|» code|integer|false|none||none|
|» message|string|false|none||none|

# Data Schema

