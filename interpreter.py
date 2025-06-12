import re

class RuivaInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.loops = []
        self.type_map = {
            'Duny': str,
            'Shaft': int,
            'Alex': int,
            'Todd': int,
            'Honey': float,
            'Priscilao': float,
            'Julie': int
        }
        self.control_structures = {
            'A Katia já foi uma grande mulher': self._handle_if,
            'KENDRA FOXTI': self._handle_for,
            'Anteriormente nessa porra': self._handle_while
        }
        self.keywords = {
            'DOMENICA': 'continue',
            'EU TENHO MAIS O QUE FAZER': 'break',
            'RETORNA ESSA MERDA': 'return'
        }

    def interpret(self, code):
        lines = self._preprocess(code)
        self._execute(lines)

    def _preprocess(self, code):
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        
        # Verificar estrutura básica do programa
        if not lines or lines[0] != 'Open the door and have fun':
            raise SyntaxError("O programa deve começar com 'Open the door and have fun'")
        if len(lines) < 2 or lines[-1] != 'uuuuh':
            raise SyntaxError("O programa deve terminar com 'uuuuh'")
        
        return lines[1:-1]  # Remove linhas de abertura/fechamento

    def _execute(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i]
            try:
                # Estruturas de controle
                handled = False
                for ctrl in self.control_structures:
                    if line.startswith(ctrl):
                        i = self.control_structures[ctrl](lines, i)
                        handled = True
                        break
                
                if handled:
                    continue
                
                # Palavras-chave
                for kw in self.keywords:
                    if kw in line:
                        action = self.keywords[kw]
                        if action == 'continue' and self.loops:
                            i = self.loops[-1]['continue']
                            continue
                        elif action == 'break' and self.loops:
                            i = self.loops[-1]['break']
                            continue
                        elif action == 'return':
                            return
                
                # Comandos básicos
                self._execute_line(line)
                i += 1
            except Exception as e:
                raise RuntimeError(f"Erro na linha {i+1}: '{line}' - {str(e)}")

    def _execute_line(self, line):
        line = line.rstrip(';').strip()
        if not line or line in ('Open the door and have fun', 'uuuuh'):
            return
        
        # DISK DUNNY (print)
        if line.startswith('DISK DUNNY(') and line.endswith(')'):
            content = line[11:-1].strip()
            if content.startswith('"') and content.endswith('"'):
                print(content[1:-1])
            else:
                try:
                    print(eval(content, {}, self.variables))
                except Exception as e:
                    raise ValueError(f"Erro ao avaliar expressão: {content}")
            return
        
        # Declaração de variável
        for type_kw in self.type_map:
            if line.startswith(type_kw):
                parts = line[len(type_kw):].strip().split('=', 1)
                var_name = parts[0].strip()
                if len(parts) > 1:
                    value = self._evaluate_expression(parts[1].strip())
                    self.variables[var_name] = self.type_map[type_kw](value)
                else:
                    self.variables[var_name] = self.type_map[type_kw]()
                return
        
        # Atribuição
        if '=' in line:
            var, expr = [p.strip() for p in line.split('=', 1)]
            if var not in self.variables:
                raise NameError(f"Variável não declarada: {var}")
            self.variables[var] = self._evaluate_expression(expr)
            return
        
        # Incremento/decremento (M++ ou M--)
        if re.match(r'^\w+\+\+$', line):
            var = line[:-2]
            if var not in self.variables:
                raise NameError(f"Variável não declarada: {var}")
            self.variables[var] += 1
            return
        elif re.match(r'^\w+--$', line):
            var = line[:-2]
            if var not in self.variables:
                raise NameError(f"Variável não declarada: {var}")
            self.variables[var] -= 1
            return

        raise SyntaxError(f"Comando não reconhecido: {line}")

    def _evaluate_expression(self, expr):
        try:
            return eval(expr, {}, self.variables)
        except Exception as e:
            raise ValueError(f"Erro ao avaliar expressão '{expr}': {str(e)}")

    def _handle_if(self, lines, start_idx):
        line = lines[start_idx]
        condition = line[line.find('(')+1:line.find(')')].strip()
        
        try:
            if self._evaluate_expression(condition):
                # Executa bloco verdadeiro
                end_idx = self._find_block_end(lines, start_idx+1)
                self._execute(lines[start_idx+1:end_idx])
                return end_idx + 1
            else:
                # Pula para depois do bloco
                end_idx = self._find_block_end(lines, start_idx+1)
                return end_idx + 1
        except Exception as e:
            raise RuntimeError(f"Erro na condição if: {str(e)}")

    def _handle_for(self, lines, start_idx):
        line = lines[start_idx]
        parts = line[line.find('(')+1:line.find(')')].split(';')
        if len(parts) != 3:
            raise SyntaxError("Sintaxe inválida do for loop")
        
        init, cond, inc = [p.strip() for p in parts]
        
        # Executa inicialização
        if init:
            self._execute_line(init)
        
        start_loop = start_idx + 1
        end_loop = self._find_block_end(lines, start_loop)
        
        self.loops.append({
            'continue': start_loop,
            'break': end_loop + 1
        })
        
        try:
            while self._evaluate_expression(cond):
                self._execute(lines[start_loop:end_loop])
                if inc:
                    self._execute_line(inc)
        except Exception as e:
            raise RuntimeError(f"Erro no loop for: {str(e)}")
        finally:
            self.loops.pop()
        
        return end_loop + 1

    def _handle_while(self, lines, start_idx):
        line = lines[start_idx]
        condition = line[line.find('(')+1:line.find(')')].strip()
        start_loop = start_idx + 1
        end_loop = self._find_block_end(lines, start_loop)
        
        self.loops.append({
            'continue': start_loop,
            'break': end_loop + 1
        })
        
        try:
            while self._evaluate_expression(condition):
                self._execute(lines[start_loop:end_loop])
        except Exception as e:
            raise RuntimeError(f"Erro no loop while: {str(e)}")
        finally:
            self.loops.pop()
        
        return end_loop + 1

    def _find_block_end(self, lines, start_idx):
        i = start_idx
        while i < len(lines):
            if lines[i].strip() == 'uuuuh':
                return i
            i += 1
        raise SyntaxError("Bloco não terminado com 'uuuuh'")