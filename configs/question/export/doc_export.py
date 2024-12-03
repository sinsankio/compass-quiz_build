from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Inches

COVER_PAGE_STYLES: dict = {
    'paragraph': {
        'alignment': WD_ALIGN_PARAGRAPH.CENTER
    }
}
SUBJECT_NAME_HEADING_STYLES: dict = {
    'paragraph': {
        'alignment': WD_ALIGN_PARAGRAPH.CENTER,
    },
    'font': {
        'name': 'Montserrat Black',
        'size': Pt(18),
        'color': RGBColor(0x1f, 0x49, 0x7d)
    }
}
PRACTICE_EXAMINATION_HEADING_STYLES: dict = {
    'paragraph': {
        'alignment': WD_ALIGN_PARAGRAPH.CENTER
    },
    'font': {
        'name': 'Montserrat Black',
        'size': Pt(16),
        'color': RGBColor(0x43, 0x43, 0x43)
    }
}
MCQ_HEADING_STYLES: dict = {
    'paragraph': {
        'alignment': WD_ALIGN_PARAGRAPH.CENTER,
    },
    'font': {
        'name': 'Montserrat Bold',
        'size': Pt(14),
        'color': RGBColor(0x1f, 0x49, 0x7d)
    }
}
MCQ_HEADING_ABBR_STYLES: dict = {
    'font': {
        'name': 'Montserrat Normal',
        'size': Pt(14),
        'color': RGBColor(0x1f, 0x49, 0x7d)
    }
}
ESSAY_QUESTION_HEADING_STYLES: dict = {
    'paragraph': {
        'alignment': WD_ALIGN_PARAGRAPH.CENTER
    },
    'font': {
        'name': 'Montserrat Bold',
        'size': Pt(14),
        'color': RGBColor(0x1f, 0x49, 0x7d)
    }
}
RESTRICTED_RESPONSE_ESSAY_QUESTION_HEADING_STYLES: dict = {
    'font': {
        'name': 'Montserrat Normal',
        'size': Pt(14),
        'color': RGBColor(0x1f, 0x49, 0x7d)
    }
}
EXTENDED_RESPONSE_ESSAY_QUESTION_HEADING_STYLES: dict = {
    'font': {
        'name': 'Montserrat Normal',
        'size': Pt(14),
        'color': RGBColor(0x1f, 0x49, 0x7d)
    }
}
ANSWER_KEY_HEADING_STYLES: dict = {
    'paragraph': {
        'alignment': WD_ALIGN_PARAGRAPH.CENTER
    },
    'font': {
        'name': 'Montserrat Bold',
        'size': Pt(16),
        'color': RGBColor(0x43, 0x43, 0x43)
    }
}
EXPORT_FILE_SAVE_DIR_PATH: str = 'api/doc_exports'
COVER_IMAGE_METADATA: dict = {
    'filepath': 'resources/images/cover.png',
    'width': Inches(6.28),
    'height': Inches(6.90)
}
