import pytest
from main import EnteLexer

test_cases = [
    {
        "name": "Test Case 1",
        "input": """
program programa1;
var a, b : int; 
    main {
        a = 1;
        b = -a;            
    } end
""",
        "expected": [
            ("PROGRAM", "program"),
            ("ID", "programa1"),
            ("SEMICOLON", ";"),
            ("VAR", "var"),
            ("ID", "a"),
            ("COMMA", ","),
            ("ID", "b"),
            ("COLON", ":"),
            ("INT", "int"),
            ("SEMICOLON", ";"),
            ("MAIN", "main"),
            ("LBRACE", "{"),
            ("ID", "a"),
            ("ASSIGN", "="),
            ("NUMBER", "1"),
            ("SEMICOLON", ";"),
            ("ID", "b"),
            ("ASSIGN", "="),
            ("MINUS", "-"),
            ("ID", "a"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
            ("END", "end"),
        ],
    },
    {
        "name": "Test Case 2",
        "input": """
program programa2 ;
    var b : int;
    main {  
        b = 5;
    } end
""",
        "expected": [
            ("PROGRAM", "program"),
            ("ID", "programa2"),
            ("SEMICOLON", ";"),
            ("VAR", "var"),
            ("ID", "b"),
            ("COLON", ":"),
            ("INT", "int"),
            ("SEMICOLON", ";"),
            ("MAIN", "main"),
            ("LBRACE", "{"),
            ("ID", "b"),
            ("ASSIGN", "="),
            ("NUMBER", "5"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
            ("END", "end"),
        ],
    },
    {
        "name": "Test Case 3",
        "input": """
program programa3;
    main {
        printf("TEST_TEXT" );
    } end
""",
        "expected": [
            ("PROGRAM", "program"),
            ("ID", "programa3"),
            ("SEMICOLON", ";"),
            ("MAIN", "main"),
            ("LBRACE", "{"),
            ("PRINTF", "printf"),
            ("LPAREN", "("),
            ("STRING", "TEST_TEXT"),
            ("RPAREN", ")"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
            ("END", "end"),
        ],
    },
    {
        "name": "Test Case 4",
        "input": """
program programa4;
    var global1, global2 : int;
    
    void funcion1 (x : float, y : float)[
        var a, b, c : float;
        {
            a = x * 10;
            b = y * 20;
            if (a / 5 < a * 5) {
                c = 100;
            } else {
                c = 0;
            };
            printf(c);
        }
    ];
    main {
        global1 = 1;
        global2 = 1;
        funcion1(global1, global2); 
     } end
""",
        "expected": [
            ("PROGRAM", "program"),
            ("ID", "programa4"),
            ("SEMICOLON", ";"),
            ("VAR", "var"),
            ("ID", "global1"),
            ("COMMA", ","),
            ("ID", "global2"),
            ("COLON", ":"),
            ("INT", "int"),
            ("SEMICOLON", ";"),
            ("VOID", "void"),
            ("ID", "funcion1"),
            ("LPAREN", "("),
            ("ID", "x"),
            ("COLON", ":"),
            ("FLOAT", "float"),
            ("COMMA", ","),
            ("ID", "y"),
            ("COLON", ":"),
            ("FLOAT", "float"),
            ("RPAREN", ")"),
            ("LBRACKET", "["),
            ("VAR", "var"),
            ("ID", "a"),
            ("COMMA", ","),
            ("ID", "b"),
            ("COMMA", ","),
            ("ID", "c"),
            ("COLON", ":"),
            ("FLOAT", "float"),
            ("SEMICOLON", ";"),
            ("LBRACE", "{"),
            ("ID", "a"),
            ("ASSIGN", "="),
            ("ID", "x"),
            ("TIMES", "*"),
            ("NUMBER", "10"),
            ("SEMICOLON", ";"),
            ("ID", "b"),
            ("ASSIGN", "="),
            ("ID", "y"),
            ("TIMES", "*"),
            ("NUMBER", "20"),
            ("SEMICOLON", ";"),
            ("IF", "if"),
            ("LPAREN", "("),
            ("ID", "a"),
            ("DIVIDE", "/"),
            ("NUMBER", "5"),
            ("LESSER", "<"),
            ("ID", "a"),
            ("TIMES", "*"),
            ("NUMBER", "5"),
            ("RPAREN", ")"),
            ("LBRACE", "{"),
            ("ID", "c"),
            ("ASSIGN", "="),
            ("NUMBER", "100"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
            ("ELSE", "else"),
            ("LBRACE", "{"),
            ("ID", "c"),
            ("ASSIGN", "="),
            ("NUMBER", "0"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
            ("SEMICOLON", ";"),
            ("PRINTF", "printf"),
            ("LPAREN", "("),
            ("ID", "c"),
            ("RPAREN", ")"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
            ("RBRACKET", "]"),
            ("SEMICOLON", ";"),
            ("MAIN", "main"),
            ("LBRACE", "{"),
            ("ID", "global1"),
            ("ASSIGN", "="),
            ("NUMBER", "1"),
            ("SEMICOLON", ";"),
            ("ID", "global2"),
            ("ASSIGN", "="),
            ("NUMBER", "1"),
            ("SEMICOLON", ";"),
            ("ID", "funcion1"),
            ("LPAREN", "("),
            ("ID", "global1"),
            ("COMMA", ","),
            ("ID", "global2"),
            ("RPAREN", ")"),
            ("SEMICOLON", ";"),
            ("RBRACE", "}"),
            ("END", "end"),
        ],
    },
    {
        "name": "Simple Expression",
        "input": "x = 3 + 42 * (s - t)",
        "expected": [
            ("ID", "x"),
            ("ASSIGN", "="),
            ("NUMBER", "3"),
            ("PLUS", "+"),
            ("NUMBER", "42"),
            ("TIMES", "*"),
            ("LPAREN", "("),
            ("ID", "s"),
            ("MINUS", "-"),
            ("ID", "t"),
            ("RPAREN", ")"),
        ],
    },
]


@pytest.mark.parametrize("case", test_cases, ids=[case["name"] for case in test_cases])
def test_lexer(case):
    lexer = EnteLexer()
    tokens = list(lexer.tokenize(case["input"]))
    assert [(tok.type, tok.value) for tok in tokens] == case["expected"]
