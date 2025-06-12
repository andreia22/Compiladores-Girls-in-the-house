import sys
import os

def find_ruiva_file(filename):
    # Verifica em vários locais possíveis
    paths_to_try = [
        filename,
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join('examples', filename),
        os.path.join('test', filename)
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            return path
    return None

def main():
    if len(sys.argv) < 2:
        print("Por favor, especifique um arquivo .ruiva")
        return
    
    filepath = find_ruiva_file(sys.argv[1])
    if not filepath:
        print(f"Arquivo {sys.argv[1]} não encontrado em:")
        print("\n".join(paths_to_try))
        return
    
    from interpreter import RuivaInterpreter
    with open(filepath, 'r') as f:
        code = f.read()
    
    RuivaInterpreter().interpret(code)

if __name__ == "__main__":
    main()