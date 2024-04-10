from django.db import models

class Tournament(models.Model):
    pass

# tipos de campeonatos:

# 1) pontos corridos
# - todos têm o mesmo número de jogos e todos enfrentam todos - deixar 2x padrão?
# - o vencedor ganha 3 pontos
# - empate cada um ganha 1 ponto

# 2) mata-mata
# quem ganhar segue pra próxima fase
# separado em fases
# precisa de um número par de equipes ?
# estrturar as chaves: Final, Semi-Final (4), quartas de final (8), oitavas de final 16

# 3) grupos + mata-mata
# - group size - aplica pontos corridos
# regra de classificação
# mata-mata

# critério de desempate: a soma de pontos feitos
# se ainda assim tiver empate, uma última prtida no formato do pong original
