import { TournamentType } from "../../contracts/game/tournament.js";

export const setTournamentFormDynamicBehavior = () => {
  const tournamentTypeField = document.getElementById("id_tournament_type");
  tournamentTypeField.addEventListener("change", updateTournamentTypeFields);

  const addPlayerButton = document.getElementById("add-player-btn");
  addPlayerButton.addEventListener("click", addPlayer);

  updateDeleteEvents();
};

const updateTournamentTypeFields = () => {
  const tournamentTypeField = document.getElementById("id_tournament_type");
  const numberOfRoundsField = document.getElementById("id_number_of_rounds");
  const numberOfPlayersField = document.getElementById("id_number_of_players");
  const roundRobinForms = document.getElementById("round-robin-forms");
  const backup = document.getElementById("players-form-backup");
  const addPlayerButton = document.getElementById("add-player-btn");

  numberOfPlayersField.disabled = true;
  if (tournamentTypeField.value === TournamentType.ROUND_ROBIN) {
    addPlayerButton.classList.remove("d-none");
    numberOfRoundsField.disabled = true;
    numberOfRoundsField.required = false;
    roundRobinForms.innerHTML = backup.innerHTML;
    backup.textContent = "";

    const number_of_players =
      2 + roundRobinForms.getElementsByTagName("li").length;
    const number_of_rounds = number_of_players - 1 + (number_of_players % 2);
    numberOfPlayersField.setAttribute("value", number_of_players);
    numberOfRoundsField.setAttribute("value", number_of_rounds);
  } else if (tournamentTypeField.value === TournamentType.CHALLENGE) {
    addPlayerButton.classList.add("d-none");
    numberOfRoundsField.disabled = false;
    numberOfRoundsField.required = true;
    numberOfRoundsField.setAttribute("value", "");
    numberOfPlayersField.setAttribute("value", 2);
    backup.innerHTML = roundRobinForms.innerHTML;
    roundRobinForms.textContent = "";
  }
};

const addPlayer = (e) => {
  e.preventDefault();
  const playerBaseForm = document
    .getElementById("player-base-form")
    .getElementsByTagName("li")[0];
  const roundRobinForms = document.getElementById("round-robin-forms");
  roundRobinForms.appendChild(playerBaseForm.cloneNode(true));

  const numberOfPlayersField = document.getElementById("id_number_of_players");
  const number_of_players = Number(numberOfPlayersField.value) + 1;
  numberOfPlayersField.setAttribute("value", number_of_players);

  const numberOfRoundsField = document.getElementById("id_number_of_rounds");
  const number_of_rounds = number_of_players - 1 + (number_of_players % 2);
  numberOfRoundsField.setAttribute("value", number_of_rounds);

  updateDeleteEvents();
};

const deletePlayer = (e) => {
  e.preventDefault();
  e.srcElement.closest("li").remove();

  const roundRobinForms = document.getElementById("round-robin-forms");
  const number_of_players =
    2 + roundRobinForms.getElementsByTagName("li").length;
  const number_of_rounds = number_of_players - 1 + (number_of_players % 2);

  const numberOfRoundsField = document.getElementById("id_number_of_rounds");
  const numberOfPlayersField = document.getElementById("id_number_of_players");
  numberOfPlayersField.setAttribute("value", number_of_players);
  numberOfRoundsField.setAttribute("value", number_of_rounds);
};

const updateDeleteEvents = () => {
  const deletePlayerButtons = document.getElementsByClassName("delete-player");
  for (let i = 0; i < deletePlayerButtons.length; i++)
    deletePlayerButtons[i].addEventListener("click", deletePlayer);
};
