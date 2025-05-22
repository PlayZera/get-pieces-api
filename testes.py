import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.tests.services.test_google_pse_service import Teste_BuscaPorItemGoogle


if __name__ == "__main__":
        print("Iniciando testes unitários")
        Teste_BuscaPorItemGoogle("AIzaSyBcoU2G0HSM5cqIjCXg8CY0ahROHlJVrDc", 
                                 "040a29c7405b54f2c",
                                 "BOTINA SEG. S/BIQUEIRA N.35",
                                 10) 