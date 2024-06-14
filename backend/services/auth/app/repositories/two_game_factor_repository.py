from ..dtos.validate_game_2factor_code_dto import ValidateGame2FactorCodeDto
from ..models.two_factor_game import TwoFactorGame
from ..interfaces.repositories.two_factor_game_repository import ITwoFactorGameRepository


class TwoFactorRepository(ITwoFactorGameRepository):

    async def add_two_factor(self, two_factor: TwoFactorGame) -> TwoFactorGame:
        return await TwoFactorGame.objects.acreate(
          code=two_factor.code,
          user_receiver_id=two_factor.user_receiver_id,
          user_requester_id=two_factor.user_requester_id,
          game_type=two_factor.game_type,
          game_id=two_factor.game_id,
        )

    async def delete_two_factor(self, id: str) -> bool:
        return await TwoFactorGame.objects.filter(id=id).adelete()

    async def find_two_factor_by_game_details(self, two_factor_game_dto: ValidateGame2FactorCodeDto) -> TwoFactorGame:
        try:
            two_factor_game_list = []
            for user_receiver_id in two_factor_game_dto.user_receiver_ids:
                tw_factor_game = await TwoFactorGame.objects.aget(
                    game_id=two_factor_game_dto.game_id,
                    user_receiver_id=user_receiver_id, user_requester_id=two_factor_game_dto.user_requester_id)
                two_factor_game_list.append(tw_factor_game)
            return two_factor_game_list
        except TwoFactorGame.DoesNotExist:
            return None

    async def delete_two_factor_by_game_details(self, two_factor_game_dto: ValidateGame2FactorCodeDto) -> bool:
        try:
            for user_receiver_id in two_factor_game_dto.user_receiver_ids:
                await TwoFactorGame.objects.filter(
                    game_id=two_factor_game_dto.game_id,
                    user_receiver_id=user_receiver_id, user_requester_id=two_factor_game_dto.user_requester_id).adelete()
        except TwoFactorGame.DoesNotExist:
            return False
