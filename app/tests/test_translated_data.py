TRANSLATED_WORD = 'targetword'

TRANSLATED_DEFINITIONS = [[['part of speech', [
    ['definition 1', None, True],
    ['definition 2', 'definition example', True, None, [['domain1'], ['domain2']]],
    ['definition 3', 'definition example', True, None, [['domain3']]],
    ['definition 4', None, True, None, None, [[[['synonym 1'],
                                                ['synonym 2'],
                                                ['synonym 3']]],
                                              [[['domain specific synonym 1'],
                                                ['domain specific synonym 2']], [['specific domain']]]]]
]]]]

TRANSLATED_EXAMPLES = [[
    [None, 'example 1'],
    [None, 'example 2'],
    [None, 'example <b>3</b>'],
]]

_TRANSLATION_FREQUENCY_NUMBER: int = 1

TRANSLATED_TRANSLATIONS = [[
    ['part of speech', [
        ['translation 1', None, ['source language word'], _TRANSLATION_FREQUENCY_NUMBER, True],
        ['translation 2', None, ['source language word'], _TRANSLATION_FREQUENCY_NUMBER, True]],
        'target',
        'source']
]]

PARSED_TRANSLATIONS = [{
    'speech_part': 'part of speech',
    'values': ['translation 1', 'translation 2']
}]

PARSED_EXAMPLES = [
    'example 1',
    'example 2',
    'example 3',
]

PARSED_DEFINITIONS = [{
    'speech_part': 'part of speech',
    'values': [
        {'value': 'definition 1'},
        {
            'value': 'definition 2',
            'example': 'definition example',
            'domains': ['domain1', 'domain2'],
        },
        {
            'value': 'definition 3',
            'example': 'definition example',
            'domains': ['domain3']
        },
        {
            'value': 'definition 4',
            'synonyms': [
                {
                    'type': 'general',
                    'values': ['synonym 1', 'synonym 2', 'synonym 3']
                },
                {
                    'type': 'specific domain',
                    'values': [
                        'domain specific synonym 1',
                        'domain specific synonym 2'
                    ]
                }
            ]
        },
    ]
}]
