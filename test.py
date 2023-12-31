import os

from regula.documentreader.webclient import *

host = os.getenv("z", "http://94.158.52.55:19880/")

with open("images/2.jpg", "rb") as f:
    input_image = f.read()

with DocumentReaderApi(host) as api:
    params = ProcessParams(
        scenario=Scenario.FULL_PROCESS,
        result_type_output=[
            # actual results
            Result.STATUS, Result.AUTHENTICITY, Result.TEXT, Result.IMAGES,
            Result.DOCUMENT_TYPE, Result.DOCUMENT_TYPE_CANDIDATES, Result.IMAGE_QUALITY,
            Result.DOCUMENT_POSITION,
            # legacy results
            Result.MRZ_TEXT, Result.VISUAL_TEXT, Result.BARCODE_TEXT, Result.RFID_TEXT,
            Result.VISUAL_GRAPHICS, Result.BARCODE_GRAPHICS, Result.RFID_GRAPHICS,
            Result.LEXICAL_ANALYSIS
        ]
    )
    request = RecognitionRequest(process_params=params, images=[input_image])
    response = api.process(request)

    # status examples
    response_status = response.status
    doc_overall_status = "valid" if response_status.overall_status == CheckResult.OK else "not valid"

    # text fields example
    doc_number_field = response.text.get_field(TextFieldType.DOCUMENT_NUMBER)
    doc_number_field_by_name = response.text.get_field_by_name("Document Number")
    doc_number_mrz = doc_number_field.get_value()
    doc_number_visual = doc_number_field.get_value(Source.VISUAL)
    doc_number_visual_validity = doc_number_field.source_validity(Source.VISUAL)
    doc_number_mrz_validity = doc_number_field.source_validity(Source.MRZ)
    doc_number_mrz_visual_matching = doc_number_field.cross_source_comparison(Source.MRZ, Source.VISUAL)

    doc_authenticity = response.authenticity()

    doc_ir_b900 = doc_authenticity.ir_b900_checks \
        if doc_authenticity is not None else None

    doc_ir_b900_blank = doc_ir_b900.checks_by_element(SecurityFeatureType.BLANK) \
        if doc_authenticity is not None else None

    doc_image_pattern = doc_authenticity.image_pattern_checks \
        if doc_authenticity is not None else None

    doc_image_pattern_blank = doc_image_pattern.checks_by_element(SecurityFeatureType.BLANK) \
        if doc_authenticity is not None else None

    # images fields example
    document_image = response.images.get_field(GraphicFieldType.DOCUMENT_FRONT).get_value()
    portrait_from_visual = response.images.get_field(GraphicFieldType.PORTRAIT).get_value(Source.VISUAL)
    with open('portrait.jpg', 'wb') as f:
        f.write(portrait_from_visual)
    with open('document-image.jpg', 'wb') as f:
        f.write(document_image)

    print("""
    ---------------------------------------------------------------------------
                        Web API version: {ping_version}
    ---------------------------------------------------------------------------
                   Document Overall Status: {doc_overall_status}
                    Document Number Visual: {doc_number_visual}
                       Document Number MRZ: {doc_number_mrz}
        Validity Of Document Number Visual: {doc_number_visual_validity}
           Validity Of Document Number MRZ: {doc_number_mrz_validity}
              MRZ-Visual values comparison: {doc_number_mrz_visual_matching}
    ---------------------------------------------------------------------------
    """.format(
        ping_version=api.ping().version,
        doc_overall_status=doc_overall_status, doc_number_visual=doc_number_visual,
        doc_number_mrz=doc_number_mrz, doc_number_visual_validity=doc_number_mrz_validity,
        doc_number_mrz_validity=doc_number_mrz_validity, doc_number_mrz_visual_matching=doc_number_mrz_visual_matching,
    ))