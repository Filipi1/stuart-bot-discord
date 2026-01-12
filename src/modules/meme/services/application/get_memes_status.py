import discord
from datetime import datetime
from modules.meme.dtos.fetch_current_memes_count.fetch_memes_status_response_dto import (
    FetchMemesStatusResponseDto,
)
from modules.meme.services.domain.fetch_memes_status_service import (
    FetchMemesStatusDomainService,
)
from modules.shared.adapters import DomainService


class GetMemesStatusApplicationService(DomainService):
    def __init__(
        self,
        fetch_memes_status_service: FetchMemesStatusDomainService,
    ):
        self.__fetch_memes_status_service = fetch_memes_status_service
        super().__init__(GetMemesStatusApplicationService.__name__)

    def __format_date(self, date_str: str) -> str:
        """Formata a data de ISO para 'Meme criado em DD/MM/YYYY às HH:MM:SS'
        
        Suporta múltiplos formatos ISO:
        - 2022-09-11T21:00:08
        - 2022-09-11T21:00:08.668859
        - 2022-09-11T21:00:08Z
        - 2022-09-11 21:00:08
        - 2022-09-11 21:00:08.668859
        """
        try:
            # Normaliza a string removendo espaços extras
            date_str = date_str.strip()
            
            # Remove o 'Z' do final se existir (timezone UTC)
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            
            # Substitui espaço por 'T' se necessário (formato ISO padrão)
            # datetime.fromisoformat() aceita espaço, mas 'T' é mais seguro
            if ' ' in date_str and 'T' not in date_str:
                date_str = date_str.replace(' ', 'T', 1)
            
            # Parse da data ISO (fromisoformat suporta frações de segundos automaticamente)
            dt = datetime.fromisoformat(date_str)
            formatted_date = dt.strftime("%d/%m/%Y às %H:%M:%S")
            return f"Meme criado em {formatted_date}"
        except (ValueError, AttributeError) as e:
            self.logger.error(f"Erro ao formatar data {date_str}: {e}")
            return date_str

    async def process(self) -> discord.Embed:
        response: FetchMemesStatusResponseDto = (
            await self.__fetch_memes_status_service.process()
        )
        self.logger.dict_to_table(response.model_dump())
        embed = discord.Embed(title="🎲 Status dos memes", color=0xFF6B6B)
        embed.add_field(name="Total de memes", value=response.total_memes)
        
        oldest_date_value = (
            self.__format_date(response.oldest_unsorted_meme_date)
            if response.oldest_unsorted_meme_date
            else "Todos os memes já foram sorteados"
        )
        embed.add_field(
            name="Meme mais antigo que ainda não foi sorteado",
            value=oldest_date_value,
            inline=False,
        )
        embed.add_field(
            name="Quantidade de memes que ainda não foram sorteados",
            value=response.unsorted_memes_count,
            inline=False,
        )
        embed.add_field(
            name="Meme mais sorteado", value=response.most_sorted_meme.title
        )
        return embed
