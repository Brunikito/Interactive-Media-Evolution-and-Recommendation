import pandas as pd
import numpy as np
import os
from datetime import time, datetime, timedelta
from src import DATA_PATH

desired_countries = [
    'CRI', 'MEX', 'CAN', 'COL', 'ECU', 'PER', 'USA', 'CHL', 'ARG', 
    'BRA', 'GBR', 'IRL', 'PRT', 'AUT', 'BEL', 'CHE', 'CZE', 'DEU', 
    'DNK', 'ESP', 'FRA', 'HRV', 'HUN', 'ITA', 'LUX', 'MAR', 'NLD', 
    'NOR', 'POL', 'SWE', 'SVK', 'BGR', 'CYP', 'EST', 'EGY', 'FIN', 
    'GRC', 'ISR', 'LTU', 'LVA', 'ROU', 'UKR', 'ZAF', 'RUS', 'SAU', 
    'TUR', 'ARE', 'IND', 'IDN', 'THA', 'VNM', 'CHN', 'HKG', 'MYS', 
    'PHL', 'SGP', 'TWN', 'JPN', 'KOR', 'AUS', 'NZL'
    ]

country_to_iso3 = {
    'lv': 'LVA', 'lu': 'LUX', 'il': 'ISR', 'fr': 'FRA', 'cn': 'CHN', 
    'sa': 'SAU', 'co': 'COL', 'lt': 'LTU', 'th': 'THA', 'cy': 'CYP', 
    'hk': 'HKG', 'au': 'AUS', 'gr': 'GRC', 'ec': 'ECU', 'cr': 'CRI', 
    'cl': 'CHL', 'ma': 'MAR', 'nl': 'NLD', 'pt': 'PRT', 'ru': 'RUS', 
    'hu': 'HUN', 'tr': 'TUR', 'mx': 'MEX', 'eg': 'EGY', 'be': 'BEL', 
    'ro': 'ROU', 'dk': 'DNK', 'kr': 'KOR', 'se': 'SWE', 'fi': 'FIN', 
    'ua': 'UKR', 'ar': 'ARG', 'vn': 'VNM', 'de': 'DEU', 'br': 'BRA', 
    'bg': 'BGR', 'my': 'MYS', 'ph': 'PHL', 'gb': 'GBR', 'ch': 'CHE', 
    'it': 'ITA', 'at': 'AUT', 'sk': 'SVK', 'ca': 'CAN', 'ae': 'ARE', 
    'tw': 'TWN', 'pe': 'PER', 'nz': 'NZL', 'hr': 'HRV', 'ie': 'IRL', 
    'za': 'ZAF', 'sg': 'SGP', 'us': 'USA', 'es': 'ESP', 'cz': 'CZE', 
    'ee': 'EST', 'id': 'IDN', 'pl': 'POL', 'no': 'NOR', 'jp': 'JPN', 
    'in': 'IND'
    }

timezone_map = {'CRI': 'UTC -6', 'MEX': 'UTC -6', 'CAN': 'UTC -5', 
                'COL': 'UTC -5', 'ECU': 'UTC -5', 'PER': 'UTC -5', 
                'USA': 'UTC -5', 'CHL': 'UTC -4', 'ARG': 'UTC -3', 
                'BRA': 'UTC -3', 'GBR': 'UTC +0', 'IRL': 'UTC +0', 
                'PRT': 'UTC +0', 'AUT': 'UTC +1', 'BEL': 'UTC +1', 
                'CHE': 'UTC +1', 'CZE': 'UTC +1', 'DEU': 'UTC +1', 
                'DNK': 'UTC +1', 'ESP': 'UTC +1', 'FRA': 'UTC +1', 
                'HRV': 'UTC +1', 'HUN': 'UTC +1', 'ITA': 'UTC +1', 
                'LUX': 'UTC +1', 'MAR': 'UTC +1', 'NLD': 'UTC +1', 
                'NOR': 'UTC +1', 'POL': 'UTC +1', 'SWE': 'UTC +1', 
                'SVK': 'UTC +1', 'BGR': 'UTC +2', 'CYP': 'UTC +2', 
                'EST': 'UTC +2', 'EGY': 'UTC +2', 'FIN': 'UTC +2', 
                'GRC': 'UTC +2', 'ISR': 'UTC +2', 'LTU': 'UTC +2', 
                'LVA': 'UTC +2', 'ROU': 'UTC +2', 'UKR': 'UTC +2', 
                'ZAF': 'UTC +2', 'RUS': 'UTC +3', 'SAU': 'UTC +3', 
                'TUR': 'UTC +3', 'ARE': 'UTC +4', 'IND': 'UTC +5:30', 
                'IDN': 'UTC +7', 'THA': 'UTC +7', 'VNM': 'UTC +7', 
                'CHN': 'UTC +8', 'HKG': 'UTC +8', 'MYS': 'UTC +8', 
                'PHL': 'UTC +8', 'SGP': 'UTC +8', 'TWN': 'UTC +8', 
                'JPN': 'UTC +9', 'KOR': 'UTC +9', 'AUS': 'UTC +10',
                'NZL': 'UTC +12'}

hipercategories_examples = {
    'Tecnologia': [
        ('Desenvolvedor de software', 'Tecnologia'),
        ('Engenheiro de dados', 'Tecnologia'),
        ('Arquiteto de TI', 'Tecnologia'),
        ('Administrador de redes', 'Tecnologia'),
        ('Analista de segurança', 'Tecnologia')
    ],
    'Saúde': [
        ('Médico', 'Saúde'),
        ('Enfermeiro', 'Saúde'),
        ('Psicólogo', 'Saúde'),
        ('Dentista', 'Saúde'),
        ('Fisioterapeuta', 'Saúde')
    ],
    'Moda': [
        ('Designer de moda', 'Moda'),
        ('Estilista', 'Moda'),
        ('Modelista', 'Moda'),
        ('Consultor de estilo', 'Moda'),
        ('Fotógrafo de moda', 'Moda')
    ],
    'Militar': [
        ('Oficial', 'Militar'),
        ('Praça', 'Militar'),
        ('Policial oficial', 'Militar'),
        ('Policial praça', 'Militar'),
        ('Bombeiro', 'Militar')
    ],
    'Gastronomia': [
        ('Chef de cozinha', 'Gastronomia'),
        ('Garçom', 'Gastronomia'),
        ('Cozinheiro', 'Gastronomia'),
        ('Barman', 'Gastronomia'),
        ('Padeiro', 'Gastronomia')
    ],
    'Entretenimento': [
        ('Ator', 'Entretenimento'),
        ('Cineasta', 'Entretenimento'),
        ('Produtor de cinema', 'Entretenimento'),
        ('Apresentador', 'Entretenimento')
    ],
    'Esportes': [
        ('Jogador de futebol', 'Esportes'),
        ('Atleta olímpico', 'Esportes'),
        ('Treinador de futebol', 'Esportes'),
        ('Árbitro de futebol', 'Esportes'),
        ('Atleta de basquete', 'Esportes')
    ],
    'Educação': [
        ('Estudante pré-escola', 'Educação'),
        ('Estudante ensino fundamental I', 'Educação'),
        ('Estudante ensino fundamental II', 'Educação'),
        ('Estudante ensino médio', 'Educação'),
        ('Estudante universitário', 'Educação'),
        ('Professor pré-escola', 'Educação'),
        ('Professor ensino fundamental I', 'Educação'),
        ('Professor ensino fundamental II', 'Educação'),
        ('Professor ensino médio', 'Educação'),
        ('Professor universitário', 'Educação')
    ],
    'Ciências': [
        ('Biólogo', 'Ciências'),
        ('Físico', 'Ciências'),
        ('Químico', 'Ciências'),
        ('Astrônomo', 'Ciências'),
        ('Geólogo', 'Ciências')
    ],
    'Música': [
        ('Músico', 'Música'),
        ('Compositor', 'Música'),
        ('Maestro', 'Música'),
        ('Cantor', 'Música'),
        ('Pianista', 'Música')
    ],
    'Arte': [
        ('Artista plástico', 'Arte'),
        ('Pintor', 'Arte'),
        ('Escultor', 'Arte'),
        ('Fotógrafo', 'Arte'),
        ('Ilustrador', 'Arte')
    ],
    'Finanças': [
        ('Contador', 'Finanças'),
        ('Analista financeiro', 'Finanças'),
        ('Consultor financeiro', 'Finanças'),
        ('Auditor', 'Finanças'),
        ('Economista', 'Finanças')
    ],
    'Engenharia': [
        ('Engenheiro civil', 'Engenharia'),
        ('Engenheiro elétrico', 'Engenharia'),
        ('Engenheiro mecânico', 'Engenharia'),
        ('Engenheiro de produção', 'Engenharia'),
        ('Engenheiro ambiental', 'Engenharia')
    ],
    'Política': [
        ('Presidente', 'Política'),
        ('Senador', 'Política'),
        ('Deputado', 'Política'),
        ('Governador', 'Política'),
        ('Vereador', 'Política')
    ],
    'Direito': [
        ('Advogado', 'Direito'),
        ('Juiz', 'Direito'),
        ('Promotor de justiça', 'Direito'),
        ('Defensor público', 'Direito'),
        ('Desembargador', 'Direito')
    ],
    'Prestação de Serviços': [
        ('Barbeiro', 'Prestação de Serviços'),
        ('Lixeiro', 'Prestação de Serviços'),
        ('Garçom', 'Prestação de Serviços'),
        ('Recepcionista', 'Prestação de Serviços'),
        ('Motorista de táxi', 'Prestação de Serviços')
    ],
    'Comunicação': [
        ('Jornalista', 'Comunicação'),
        ('Redator', 'Comunicação'),
        ('Locutor', 'Comunicação'),
        ('Roteirista', 'Comunicação'),
        ('Publicitário', 'Comunicação')
    ],
    'Agronegócio': [
        ('Agrônomo', 'Agronegócio'),
        ('Zootecnista', 'Agronegócio'),
        ('Veterinário', 'Agronegócio'),
        ('Engenheiro agrônomo', 'Agronegócio'),
        ('Pecuarista', 'Agronegócio')
    ],
    'Turismo': [
        ('Guia turístico', 'Turismo'),
        ('Agente de viagens', 'Turismo'),
        ('Recepcionista de hotel', 'Turismo'),
        ('Gerente de hotel', 'Turismo'),
        ('Consultor de turismo', 'Turismo')
    ],
    'Construção Civil': [
        ('Pedreiro', 'Construção Civil'),
        ('Carpinteiro', 'Construção Civil'),
        ('Engenheiro civil', 'Construção Civil'),
        ('Mestre de obras', 'Construção Civil'),
        ('Ajudante de pedreiro', 'Construção Civil')
    ],
    'Programação': [
        ('Programador de software', 'Programação'),
        ('Desenvolvedor front-end', 'Programação'),
        ('Desenvolvedor back-end', 'Programação'),
        ('Analista de sistemas', 'Programação'),
        ('Engenheiro de software', 'Programação')
    ],
    'Jogos': [
        ('Designer de jogos', 'Jogos'),
        ('Programador de jogos', 'Jogos'),
        ('Tester de jogos', 'Jogos'),
        ('Desenvolvedor de jogos', 'Jogos'),
        ('Produtor de jogos', 'Jogos')
    ],
    'Design': [
        ('Designer gráfico', 'Design'),
        ('Designer de interiores', 'Design'),
        ('Designer de produto', 'Design'),
        ('Designer de moda', 'Design'),
        ('Ilustrador', 'Design')
    ],
    'Gestão': [
        ('Gerente de vendas', 'Gestão'),
        ('Gestor de recursos humanos', 'Gestão'),
        ('Diretor executivo', 'Gestão'),
        ('Consultor de gestão', 'Gestão'),
        ('Coordenador de projetos', 'Gestão')
    ],
    'Segurança': [
        ('Segurança privada', 'Segurança'),
        ('Policial militar', 'Segurança'),
        ('Agente de segurança', 'Segurança'),
        ('Vigilante', 'Segurança'),
        ('Perito criminal', 'Segurança')
    ],
    'Tecnologia da Informação': [
        ('Administrador de sistemas', 'Tecnologia da Informação'),
        ('Analista de redes', 'Tecnologia da Informação'),
        ('Desenvolvedor de TI', 'Tecnologia da Informação'),
        ('Suporte técnico', 'Tecnologia da Informação'),
        ('Engenheiro de software', 'Tecnologia da Informação')
    ],
    'Logística': [
        ('Logístico', 'Logística'),
        ('Gerente de logística', 'Logística'),
        ('Coordenador de logística', 'Logística'),
        ('Motorista de transporte', 'Logística'),
        ('Supervisor de estoque', 'Logística')
    ],
    'Vendas': [
        ('Vendedor', 'Vendas'),
        ('Representante comercial', 'Vendas'),
        ('Gerente de vendas', 'Vendas'),
        ('Supervisor de vendas', 'Vendas'),
        ('Consultor de vendas', 'Vendas')
    ]
    }

horarios_trabalho = {
    'Desenvolvedor de software': time(9, 0),
    'Engenheiro de dados': time(9, 0),
    'Arquiteto de TI': time(9, 0),
    'Administrador de redes': time(9, 0),
    'Analista de segurança': time(9, 0),
    'Médico': time(7, 0),
    'Enfermeiro': time(7, 0),
    'Psicólogo': time(9, 0),
    'Dentista': time(8, 0),
    'Fisioterapeuta': time(8, 0),
    'Designer de moda': time(9, 0),
    'Estilista': time(9, 0),
    'Modelista': time(9, 0),
    'Consultor de estilo': time(9, 0),
    'Fotógrafo de moda': time(9, 0),
    'Oficial': time(5, 0),
    'Praça': time(5, 0),
    'Policial oficial': time(5, 0),
    'Policial praça': time(5, 0),
    'Bombeiro': time(5, 0),
    'Chef de cozinha': time(10, 0),
    'Garçom': time(10, 0),
    'Cozinheiro': time(10, 0),
    'Barman': time(10, 0),
    'Padeiro': time(4, 0),
    'Ator': time(9, 0),
    'Cineasta': time(9, 0),
    'Produtor de cinema': time(9, 0),
    'Apresentador': time(9, 0),
    'Jogador de futebol': time(10, 0),
    'Atleta olímpico': time(9, 0),
    'Treinador de futebol': time(9, 0),
    'Árbitro de futebol': time(10, 0),
    'Atleta de basquete': time(10, 0),
    'Estudante pré-escola': time(7, 0),
    'Estudante ensino fundamental I': time(7, 0),
    'Estudante ensino fundamental II': time(7, 0),
    'Estudante ensino médio': time(7, 0),
    'Estudante universitário': time(7, 0),
    'Professor pré-escola': time(7, 0),
    'Professor ensino fundamental I': time(7, 0),
    'Professor ensino fundamental II': time(7, 0),
    'Professor ensino médio': time(7, 0),
    'Professor universitário': time(7, 0),
    'Biólogo': time(9, 0),
    'Físico': time(9, 0),
    'Químico': time(9, 0),
    'Astrônomo': time(9, 0),
    'Geólogo': time(9, 0),
    'Músico': time(9, 0),
    'Compositor': time(9, 0),
    'Maestro': time(9, 0),
    'Cantor': time(19, 0),
    'Pianista': time(9, 0),
    'Artista plástico': time(9, 0),
    'Pintor': time(9, 0),
    'Escultor': time(9, 0),
    'Fotógrafo': time(9, 0),
    'Ilustrador': time(9, 0),
    'Contador': time(9, 0),
    'Analista financeiro': time(9, 0),
    'Consultor financeiro': time(9, 0),
    'Auditor': time(9, 0),
    'Economista': time(7, 0),
    'Engenheiro civil': time(8, 0),
    'Engenheiro elétrico': time(8, 0),
    'Engenheiro mecânico': time(8, 0),
    'Engenheiro de produção': time(8, 0),
    'Engenheiro ambiental': time(8, 0),
    'Presidente': time(9, 0),
    'Senador': time(9, 0),
    'Deputado': time(9, 0),
    'Governador': time(9, 0),
    'Vereador': time(9, 0),
    'Advogado': time(9, 0),
    'Juiz': time(9, 0),
    'Promotor de justiça': time(7, 0),
    'Defensor público': time(7, 0),
    'Desembargador': time(7, 0),
    'Barbeiro': time(7, 0),
    'Lixeiro': time(6, 0),
    'Garçom': time(10, 0),
    'Recepcionista': time(9, 0),
    'Motorista de táxi': time(8, 0),
    'Jornalista': time(9, 0),
    'Redator': time(9, 0),
    'Locutor': time(9, 0),
    'Roteirista': time(9, 0),
    'Publicitário': time(9, 0),
    'Agrônomo': time(8, 0),
    'Zootecnista': time(8, 0),
    'Veterinário': time(8, 0),
    'Engenheiro agrônomo': time(8, 0),
    'Pecuarista': time(8, 0),
    'Guia turístico': time(9, 0),
    'Agente de viagens': time(9, 0),
    'Recepcionista de hotel': time(9, 0),
    'Gerente de hotel': time(9, 0),
    'Consultor de turismo': time(9, 0),
    'Pedreiro': time(7, 0),
    'Carpinteiro': time(7, 0),
    'Engenheiro civil': time(7, 0),
    'Mestre de obras': time(7, 0),
    'Ajudante de pedreiro': time(7, 0),
    'Programador de software': time(9, 0),
    'Desenvolvedor front-end': time(9, 0),
    'Desenvolvedor back-end': time(9, 0),
    'Analista de sistemas': time(9, 0),
    'Engenheiro de software': time(9, 0),
    'Designer de jogos': time(9, 0),
    'Programador de jogos': time(9, 0),
    'Tester de jogos': time(9, 0),
    'Desenvolvedor de jogos': time(9, 0),
    'Produtor de jogos': time(9, 0),
    'Designer gráfico': time(9, 0),
    'Designer de interiores': time(9, 0),
    'Designer de produto': time(9, 0),
    'Designer de moda': time(9, 0),
    'Ilustrador': time(9, 0),
    'Gerente de vendas': time(7, 0),
    'Gestor de recursos humanos': time(7, 0),
    'Diretor executivo': time(7, 0),
    'Consultor de gestão': time(7, 0),
    'Coordenador de projetos': time(7, 0),
    'Segurança privada': time(18, 0),
    'Policial militar': time(6, 0),
    'Agente de segurança': time(6, 0),
    'Vigilante': time(18, 0),
    'Perito criminal': time(9, 0),
    'Administrador de sistemas': time(9, 0),
    'Analista de redes': time(9, 0),
    'Desenvolvedor de TI': time(9, 0),
    'Suporte técnico': time(9, 0),
    'Engenheiro de software': time(9, 0),
    'Logístico': time(8, 0),
    'Gerente de logística': time(9, 0),
    'Coordenador de logística': time(9, 0),
    'Motorista de transporte': time(8, 0),
    'Supervisor de estoque': time(8, 0),
    'Vendedor': time(9, 0),
    'Representante comercial': time(9, 0),
    'Gerente de vendas': time(9, 0),
    'Supervisor de vendas': time(9, 0),
    'Consultor de vendas': time(9, 0),
}

horas_trabalho_estimadas = {
    'Desenvolvedor de software': 8,
    'Engenheiro de dados': 8,
    'Arquiteto de TI': 8,
    'Administrador de redes': 8,
    'Analista de segurança': 8,
    'Médico': 10,
    'Enfermeiro': 12,
    'Psicólogo': 8,
    'Dentista': 8,
    'Fisioterapeuta': 8,
    'Designer de moda': 8,
    'Estilista': 8,
    'Modelista': 8,
    'Consultor de estilo': 8,
    'Fotógrafo de moda': 8,
    'Oficial': 12,
    'Praça': 12,
    'Policial oficial': 12,
    'Policial praça': 12,
    'Bombeiro': 12,
    'Chef de cozinha': 10,
    'Garçom': 8,
    'Cozinheiro': 8,
    'Barman': 8,
    'Padeiro': 8,
    'Ator': 6,
    'Cineasta': 8,
    'Produtor de cinema': 8,
    'Apresentador': 6,
    'Jogador de futebol': 8,
    'Atleta olímpico': 6,
    'Treinador de futebol': 8,
    'Árbitro de futebol': 6,
    'Atleta de basquete': 8,
    'Estudante pré-escola': 4,
    'Estudante ensino fundamental I': 4,
    'Estudante ensino fundamental II': 4,
    'Estudante ensino médio': 6,
    'Estudante universitário': 6,
    'Professor pré-escola': 4,
    'Professor ensino fundamental I': 4,
    'Professor ensino fundamental II': 4,
    'Professor ensino médio': 8,
    'Professor universitário': 6,
    'Biólogo': 8,
    'Físico': 8,
    'Químico': 8,
    'Astrônomo': 8,
    'Geólogo': 8,
    'Músico': 6,
    'Compositor': 6,
    'Maestro': 6,
    'Cantor': 6,
    'Pianista': 6,
    'Artista plástico': 6,
    'Pintor': 6,
    'Escultor': 6,
    'Fotógrafo': 8,
    'Ilustrador': 8,
    'Contador': 8,
    'Analista financeiro': 8,
    'Consultor financeiro': 8,
    'Auditor': 8,
    'Economista': 8,
    'Engenheiro civil': 8,
    'Engenheiro elétrico': 8,
    'Engenheiro mecânico': 8,
    'Engenheiro de produção': 8,
    'Engenheiro ambiental': 8,
    'Presidente': 10,
    'Senador': 8,
    'Deputado': 8,
    'Governador': 10,
    'Vereador': 8,
    'Advogado': 8,
    'Juiz': 8,
    'Promotor de justiça': 8,
    'Defensor público': 8,
    'Desembargador': 8,
    'Barbeiro': 8,
    'Lixeiro': 8,
    'Garçom': 8,
    'Recepcionista': 8,
    'Motorista de táxi': 8,
    'Jornalista': 8,
    'Redator': 8,
    'Locutor': 8,
    'Roteirista': 8,
    'Publicitário': 8,
    'Agrônomo': 8,
    'Zootecnista': 8,
    'Veterinário': 8,
    'Engenheiro agrônomo': 8,
    'Pecuarista': 8,
    'Guia turístico': 8,
    'Agente de viagens': 8,
    'Recepcionista de hotel': 8,
    'Gerente de hotel': 8,
    'Consultor de turismo': 8,
    'Pedreiro': 8,
    'Carpinteiro': 8,
    'Engenheiro civil': 8,
    'Mestre de obras': 8,
    'Ajudante de pedreiro': 8,
    'Programador de software': 8,
    'Desenvolvedor front-end': 8,
    'Desenvolvedor back-end': 8,
    'Analista de sistemas': 8,
    'Engenheiro de software': 8,
    'Designer de jogos': 8,
    'Programador de jogos': 8,
    'Tester de jogos': 8,
    'Desenvolvedor de jogos': 8,
    'Produtor de jogos': 8,
    'Designer gráfico': 8,
    'Designer de interiores': 8,
    'Designer de produto': 8,
    'Designer de moda': 8,
    'Ilustrador': 8,
    'Gerente de vendas': 8,
    'Gestor de recursos humanos': 8,
    'Diretor executivo': 8,
    'Consultor de gestão': 8,
    'Coordenador de projetos': 8,
    'Segurança privada': 8,
    'Policial militar': 12,
    'Agente de segurança': 12,
    'Vigilante': 12,
    'Perito criminal': 8,
    'Administrador de sistemas': 8,
    'Analista de redes': 8,
    'Desenvolvedor de TI': 8,
    'Suporte técnico': 8,
    'Engenheiro de software': 8,
    'Logístico': 8,
    'Gerente de logística': 8,
    'Coordenador de logística': 8,
    'Motorista de transporte': 8,
    'Supervisor de estoque': 8,
    'Vendedor': 8,
    'Representante comercial': 8,
    'Gerente de vendas': 8,
    'Supervisor de vendas': 8,
    'Consultor de vendas': 8,
}

dias_trabalhados = {
    'Desenvolvedor de software': 5,
    'Engenheiro de dados': 5,
    'Arquiteto de TI': 5,
    'Administrador de redes': 5,
    'Analista de segurança': 5,
    'Médico': 6,
    'Enfermeiro': 6,
    'Psicólogo': 5,
    'Dentista': 5,
    'Fisioterapeuta': 5,
    'Designer de moda': 5,
    'Estilista': 5,
    'Modelista': 5,
    'Consultor de estilo': 5,
    'Fotógrafo de moda': 5,
    'Oficial': 6,
    'Praça': 6,
    'Policial oficial': 6,
    'Policial praça': 6,
    'Bombeiro': 6,
    'Chef de cozinha': 6,
    'Garçom': 6,
    'Cozinheiro': 6,
    'Barman': 6,
    'Padeiro': 6,
    'Ator': 5,
    'Cineasta': 5,
    'Produtor de cinema': 5,
    'Apresentador': 5,
    'Jogador de futebol': 6,
    'Atleta olímpico': 5,
    'Treinador de futebol': 5,
    'Árbitro de futebol': 5,
    'Atleta de basquete': 6,
    'Estudante pré-escola': 5,
    'Estudante ensino fundamental I': 5,
    'Estudante ensino fundamental II': 5,
    'Estudante ensino médio': 5,
    'Estudante universitário': 5,
    'Professor pré-escola': 5,
    'Professor ensino fundamental I': 5,
    'Professor ensino fundamental II': 5,
    'Professor ensino médio': 5,
    'Professor universitário': 5,
    'Biólogo': 5,
    'Físico': 5,
    'Químico': 5,
    'Astrônomo': 5,
    'Geólogo': 5,
    'Músico': 5,
    'Compositor': 5,
    'Maestro': 5,
    'Cantor': 6,
    'Pianista': 5,
    'Artista plástico': 5,
    'Pintor': 5,
    'Escultor': 5,
    'Fotógrafo': 5,
    'Ilustrador': 5,
    'Contador': 5,
    'Analista financeiro': 5,
    'Consultor financeiro': 5,
    'Auditor': 5,
    'Economista': 5,
    'Engenheiro civil': 5,
    'Engenheiro elétrico': 5,
    'Engenheiro mecânico': 5,
    'Engenheiro de produção': 5,
    'Engenheiro ambiental': 5,
    'Presidente': 5,
    'Senador': 5,
    'Deputado': 5,
    'Governador': 5,
    'Vereador': 5,
    'Advogado': 5,
    'Juiz': 5,
    'Promotor de justiça': 5,
    'Defensor público': 5,
    'Desembargador': 5,
    'Barbeiro': 5,
    'Lixeiro': 6,
    'Recepcionista': 5,
    'Motorista de táxi': 5,
    'Jornalista': 5,
    'Redator': 5,
    'Locutor': 5,
    'Roteirista': 5,
    'Publicitário': 5,
    'Agrônomo': 5,
    'Zootecnista': 5,
    'Veterinário': 5,
    'Engenheiro agrônomo': 5,
    'Pecuarista': 5,
    'Guia turístico': 5,
    'Agente de viagens': 5,
    'Recepcionista de hotel': 5,
    'Gerente de hotel': 5,
    'Consultor de turismo': 5,
    'Pedreiro': 5,
    'Carpinteiro': 5,
    'Engenheiro civil': 5,
    'Mestre de obras': 5,
    'Ajudante de pedreiro': 5,
    'Programador de software': 5,
    'Desenvolvedor front-end': 5,
    'Desenvolvedor back-end': 5,
    'Analista de sistemas': 5,
    'Engenheiro de software': 5,
    'Designer de jogos': 5,
    'Programador de jogos': 5,
    'Tester de jogos': 5,
    'Desenvolvedor de jogos': 5,
    'Produtor de jogos': 5,
    'Designer gráfico': 5,
    'Designer de interiores': 5,
    'Designer de produto': 5,
    'Ilustrador': 5,
    'Gerente de vendas': 5,
    'Gestor de recursos humanos': 5,
    'Diretor executivo': 5,
    'Consultor de gestão': 5,
    'Coordenador de projetos': 5,
    'Segurança privada': 5,
    'Policial militar': 6,
    'Agente de segurança': 6,
    'Vigilante': 6,
    'Perito criminal': 5,
    'Administrador de sistemas': 5,
    'Analista de redes': 5,
    'Desenvolvedor de TI': 5,
    'Suporte técnico': 5,
    'Engenheiro de software': 5,
    'Logístico': 5,
    'Gerente de logística': 5,
    'Coordenador de logística': 5,
    'Motorista de transporte': 5,
    'Supervisor de estoque': 5,
    'Vendedor': 5,
    'Representante comercial': 5,
    'Gerente de vendas': 5,
    'Supervisor de vendas': 5,
    'Consultor de vendas': 5,
}

def generate_country_behavior():
    df = pd.read_table(os.path.join(DATA_PATH, 'behavior_imported', 'country_data.txt'), sep='\t', header=0, index_col=0)
    df = df[df['ISO3'].isin(desired_countries)]
    df.drop(columns=['fips', 'Capital', 'Area(in sq km)', 'tld', 'CurrencyCode', 'CurrencyName', 'Phone', 'Postal Code Format', 'Postal Code Regex', 'geonameid', 'neighbours', 'EquivalentFipsCode'], axis= 1, inplace=True)
    df.fillna('NA', inplace=True)
    df['Languages'] = df['Languages'].str.replace(r'-\w{2}', '', regex=True)
    df.reset_index(drop=True, inplace=True)
    
    def convert_to_float(utc_string):
        sign = 1 if '+' in utc_string else -1
        cleaned = utc_string.replace('UTC ', '').replace('+', '').replace('-', '')
        
        # Caso com horas inteiras (ex: UTC +5 ou UTC -3)
        if len(cleaned.split(':')) == 1:
            return sign * int(cleaned)
        
        # Caso com horas e minutos (ex: UTC +5:30)
        else:
            hours, minutes = map(int, cleaned.split(':'))
            return sign * (hours + minutes / 60)
    df['Timezone'] = df['ISO3'].map(timezone_map).apply(convert_to_float)
    total_population = df['Population'].sum()
    df['Population_Fraction'] = df['Population'] / total_population
    
    df.to_parquet(os.path.join(DATA_PATH, 'behavior_generated', 'country_data_cleaned.parquet'), index=False)
    return df

def generate_sleep_behavior():
    sleep_by_country = pd.read_json(os.path.join(DATA_PATH, 'behavior_imported', 'sleep_by_country.json'))
    sleep_generations = pd.read_json(os.path.join(DATA_PATH, 'behavior_imported', 'sleep_duration_generations.json'))
    sleep_by_country['avg_duration'] = sleep_by_country['avg_duration']/3600
    sleep_by_country['avg_snore_duration'] = sleep_by_country['avg_snore_duration']/3600
    sleep_by_country['avg_bedtime'] = sleep_by_country['avg_bedtime']*24
    sleep_by_country['avg_wakeup'] = sleep_by_country['avg_wakeup']*24
    sleep_by_country = sleep_by_country.dropna()
    
    total_users = sleep_generations['users_in_group'].sum()
    avg_duration = (sleep_generations['avg_duration']*sleep_generations['users_in_group']).sum() / total_users
    sleep_generations['relative_duration'] = sleep_generations['avg_duration'] / avg_duration
    gen_rel_duration = pd.DataFrame()
    gen_rel_duration['age_span'] = sleep_generations['age_span']
    gen_rel_duration['relative_duration'] = sleep_generations['relative_duration']
    gen_rel_duration['age_span'] = gen_rel_duration['age_span'].str.split('-').str[1].astype(int)
    sleep_country_important = sleep_by_country[['country', 'avg_duration', 'avg_bedtime', 'avg_wakeup']].copy()
    
    sleep_country_important['country'] = sleep_country_important['country'].map(country_to_iso3)
    
    # Criar uma nova tabela para armazenar os resultados
    sleep_hours_by_age_country = []

    # Iterar sobre cada país
    for _, country_row in sleep_country_important.iterrows():
        country = country_row['country']
        avg_duration = country_row['avg_duration']
        avg_bedtime = country_row['avg_bedtime']
        avg_wakeup = country_row['avg_wakeup']
        
        # Calcular o número de horas de sono por faixa etária
        for _, age_row in gen_rel_duration.iterrows():
            age_span = age_row['age_span']
            relative_duration = age_row['relative_duration']
            sleep_hours = avg_duration * relative_duration
            
            # Ajustar os horários de dormir e acordar com base na duração relativa
            adjusted_bedtime = avg_bedtime - (avg_duration - sleep_hours) / 2
            adjusted_wakeup = avg_wakeup + (avg_duration - sleep_hours) / 2
            
            # Adicionar os resultados à tabela
            sleep_hours_by_age_country.append({
                'country': country,
                'age_span': age_span,
                'sleep_hours': sleep_hours,
                'adjusted_bedtime': adjusted_bedtime,
                'adjusted_wakeup': adjusted_wakeup
            })

    # Converter a lista de resultados em um DataFrame
    sleep_hours_by_age_country = pd.DataFrame(sleep_hours_by_age_country)
    
    sleep_hours_by_age_country.to_parquet(os.path.join(DATA_PATH, 'behavior_generated', 'sleep_hours_by_age_country.parquet'), index=False)
    
    return sleep_hours_by_age_country
    
def generate_work_behavior():
    data = []
    for categoria, profissões in hipercategories_examples.items():
        for profissão, categoria in profissões:
            data.append([profissão, categoria])

    # Criar o DataFrame
    df = pd.DataFrame(data, columns=['ocupation', 'category'])
    df['ocupation'].to_list()
    df['work_time'] = df['ocupation'].map(horarios_trabalho)
    df['hours_work'] = df['ocupation'].map(horas_trabalho_estimadas)
    df['free_from_work_time'] = df.apply(
        lambda row: (datetime.combine(datetime.min, row['work_time']) + timedelta(hours=int(row['hours_work']))).time(),
        axis=1
    )
    df.drop(columns=['hours_work'], inplace=True)
    df['days_work'] = df['ocupation'].map(dias_trabalhados)
    df['work_time'] = df['work_time'].astype(str)
    df['work_time_hour'] = df['work_time'].str.split(':').str[0].astype(int)
    df['free_from_work_time'] = df['free_from_work_time'].astype(str)
    df['free_from_work_time_hour'] = df['free_from_work_time'].str.split(':').str[0].astype(int)
    df.to_parquet(os.path.join(DATA_PATH, 'behavior_generated', 'work_behavior.parquet'), index=False)
    
    return df

languages = ['abx', 'ady', 'af', 'akl', 'ar', 'as', 'av', 'ay', 'az', 'ba', 'bcl', 
             'ber', 'bg', 'bh', 'bik', 'bn', 'br', 'bua', 'ca', 'cau', 'cbk', 'ce', 
             'ceb', 'chm', 'cmn', 'co', 'cs', 'cv', 'cy', 'da', 'de', 'diq', 'doi', 
             'dta', 'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fil', 'fo', 'fr', 'frp', 
             'fy', 'ga', 'gd', 'gl', 'gn', 'gu', 'hak', 'haw', 'he', 'hi', 'hil', 'hr', 
             'hu', 'ibg', 'id', 'ilo', 'inc', 'inh', 'it', 'iu', 'ja', 'jv', 'kbd', 
             'km', 'kn', 'ko', 'kok', 'krc', 'krj', 'ks', 'ku', 'kv', 'lb', 'lt', 'lus', 
             'lv', 'mdf', 'mdh', 'mi', 'ml', 'mni', 'mns', 'mr', 'mrw', 'ms', 'msb', 
             'mta', 'mwl', 'myv', 'nan', 'nb', 'ne', 'nl', 'nn', 'no', 'nog', 'nr', 
             'nso', 'oc', 'or', 'pa', 'pag', 'pam', 'pl', 'pt', 'qu', 'rm', 'ro', 'rom', 
             'ru', 'sa', 'sah', 'sat', 'sc', 'sd', 'se', 'sgd', 'sit', 'sk', 'sl', 'sma', 
             'smn', 'sr', 'ss', 'st', 'sv', 'ta', 'te', 'th', 'tl', 'tn', 'tr', 'ts', 
             'tsg', 'tt', 'tut', 'tyv', 'udm', 'ug', 'uk', 'ur', 've', 'vi', 'war', 'wuu', 
             'xal', 'xh', 'yka', 'yue', 'za', 'zh', 'zu']

if __name__ == "__main__":
    df = generate_country_behavior()
    #generate_sleep_behavior()
    #generate_work_behavior()
    #print("Behavior data generated successfully.")

    des = np.array(desired_countries)
    array = df.set_index('ISO3').loc[des]['Languages'].values
    array_upper = [f'{{{entry.upper()}}}' for entry in array]
    #print(array_upper)
    a = "'{ES,EN}', '{ES}', '{EN,FR,IU}', '{ES}', '{ES}', '{ES,QU,AY}', '{EN,ES,HAW,FR}', '{ES}', '{ES,EN,IT,DE,FR,GN}', '{PT,ES,EN,FR}', '{EN,CY,GD}', '{EN,GA}', '{PT,MWL}', '{DE,HR,HU,SL}', '{NL,FR,DE}', '{DE,FR,IT,RM}', '{CS,SK}', '{DE}', '{DA,EN,FO,DE}', '{ES,CA,GL,EU,OC}', '{FR,FRP,BR,CO,CA,EU,OC}', '{HR,SR}', '{HU}', '{IT,DE,FR,SC,CA,CO,SL}', '{LB,DE,FR}', '{AR,BER,FR}', '{NL,FY}', '{NO,NB,NN,SE,FI}', '{PL}', '{SV,SE,SMA,FI}', '{SK,HU}', '{BG,TR,ROM}', '{EL,TR,EN}', '{ET,RU}', '{AR,EN,FR}', '{FI,SV,SMN}', '{EL,EN,FR}', '{HE,AR,EN,}', '{LT,RU,PL}', '{LV,RU,LT}', '{RO,HU,ROM}', '{UK,RU,ROM,PL,HU}', '{ZU,XH,AF,NSO,EN,TN,ST,TS,SS,VE,NR}', '{RU,TT,XAL,CAU,ADY,KV,CE,TYV,CV,UDM,TUT,MNS,BUA,MYV,MDF,CHM,BA,INH,KBD,KRC,AV,SAH,NOG}', '{AR}', '{TR,KU,DIQ,AZ,AV}', '{AR,FA,EN,HI,UR}', '{EN,HI,BN,TE,MR,TA,UR,GU,KN,ML,OR,PA,AS,BH,SAT,KS,NE,SD,KOK,DOI,MNI,SIT,SA,FR,LUS,INC}', '{ID,EN,NL,JV}', '{TH,EN}', '{VI,EN,FR,ZH,KM}', '{ZH,YUE,WUU,DTA,UG,ZA}', '{ZH,YUE,ZH,EN}', '{MS,EN,ZH,TA,TE,ML,PA,TH}', '{TL,EN,FIL,CEB,ILO,HIL,WAR,PAM,BIK,BCL,PAG,MRW,TSG,MDH,CBK,KRJ,SGD,MSB,AKL,IBG,YKA,MTA,ABX}', '{CMN,EN,MS,TA,ZH}', '{ZH,ZH,NAN,HAK}', '{JA}', '{KO,EN}', '{EN}', '{EN,MI}'"
    print(a.replace("'", ''))