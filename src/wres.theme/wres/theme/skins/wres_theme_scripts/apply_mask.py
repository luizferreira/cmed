##parameters=value, mask
#chamado por getPatientData e print_prescription
def getFormatEntities(mask):
    """
    '(dd)dd-dd' -> ['(', '', '', ')', '', '', '-', '', '', ]
    'd--d-d' -> ['', '--', '', '-', '']
    """
    result = []
    format_entity = []
    for character in mask:
        if character != 'd':
            format_entity.append(character)
        else:
            result.append(''.join(format_entity))
            format_entity = []
    return result

def format(to_format, mask):
    """
    ('123456', '(dd)dd-dd') -> '(12)34-56'
    ('123', 'd--d-d') -> '1--2-3'
    """
    format_entities = getFormatEntities(mask)
    pairs = zip(format_entities, to_format)
    parts = [''.join(pair) for pair in pairs]
    formatted = ''.join(parts)
    return formatted

if not value:
    value = ''
return format(value, mask)
