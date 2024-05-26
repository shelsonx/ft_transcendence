import gameInfoService from '../../services/gameInfoService.js';

import BaseLoggedView from '../baseLoggedView.js';

class GameInfoView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
  <div class="container-fluid main">
        <div class="containers">
            <div class="row">
                <div class="col-lg-12 mb-3">
                    <div class="container_details text-center">
                        <div class="row align-items-center justify-content-center">
                            <div class="col-md-4" id="details-medal-user">
                                <img src="static/src/img/gold_medal_star_icon.png" alt="medalha do usuário" class="details-pictures details-medal-picture">
                                <p class="mb-1" id="details-fullname">FT_TRANSCENDENCE 42 SP</p>
                                <p id="details-status">
                                     <i class="fa-solid fa-circle me-2" id="details-status-icon" style="color: #4B0082"></i>
                                    <strong id="details-status-label"></strong>
                                </p>
                            </div>
                            <div class="col-md-4" id="details-photo-user">
                                <img src="static/src/img/astronaut4.jpeg" alt="Foto do usuário" class="details-pictures details-profile-picture" id="details-photo">
                            </div>
                            <div class="col-md-4">
                                <div class="row">
                                    <div class="col"  id="details-infos-user">
                                        <div class="row mb-2">
                                            <div class="col-6 text-white" data-i18n-key="game-info--nickname">Nickname:</div>
                                            <div class="col-6 text-white" id="details-nickname">transcdc-ft</div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="col-6 text-white" data-i18n-key="game-info--scores">Scores:</div>
                                            <div class="col-6 text-white" id="details-scores">42</div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="col-6 text-white" data-i18n-key="game-info--winnings">Winnings:</div>
                                            <div class="col-6 text-white" id="details-winnings">42</div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="col-6 text-white" data-i18n-key="game-info--losses">Losses:</div>
                                            <div class="col-6 text-white" id="details-losses">0</div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="col-6 text-white" data-i18n-key="game-info--ranking">Ranking:</div>
                                            <div class="col-6 text-white" id="details-position">1º</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="containers">
            <div class="row header-row-info">
                <div class="col-8 header-info-column">
                    <i class="fas fa-info-circle header-info-icon"></i>
                    <div>
                        <p class="mb-0" data-i18n-key="game-info--info">Info</p>
                    </div>
                </div>
                <div class="col-2 header-scores-column">
                    <i class="fas fa-chart-bar me-2"></i>
                    <div>
                        <p class="mb-0" data-i18n-key="game-info--scores" id="game-info-scores-label">Scores</p>
                        <p class="mb-0" id="total_scores"></p>
                    </div>
                </div>
                <div class="col-2 header-players-column">
                    <i class="fas fa-users me-2"></i>
                    <div>
                        <p class="mb-0" data-i18n-key="game-info--players">Players</p>
                        <p class="mb-0" id="total_players"></p>
                    </div>
                </div>
            </div>
        </div>
        <div class="containers users-list" id="containers"></div>
    </div>

`

google.charts.load('current', {'packages':['corechart']});
function drawChart(chartDiv, response) {
    var data = google.visualization.arrayToDataTable([
        ['User', 'Performance'],
        ['Winnings', response.user.winnings],
        ['Losses', response.user.losses],
    ]);

    var options = {
        title: 'User Performance',
        legend: {
            textStyle: {
                color: 'white',
            }
        },
        backgroundColor: 'none',
        titleTextStyle: {
            color: 'white',
            fontSize: 10
        },
        pieStartAngle: 100,
        colors: ['#652417', '#381718'],
        fontName: 'Turret Road',
        is3D: true,
    };

    var chart = new google.visualization.PieChart(chartDiv);

    chart.draw(data, options);
}

function drawChartMedalRaking(chartDiv, response) {
    var data = google.visualization.arrayToDataTable([
        ["Medals", "Scores", { role: "style" } ],
        ["Bronze", 500, "#CD7F32"],
        ["Silver", 2000, "#d7ded9"],
        ["Gold", 5000, "#daa520"],
    ]);

    data.addRow([response.user.nickname, response.user.scores, "#652417"]);
    data.sort([{column: 1}]);

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
        {
            calc: "stringify",
            sourceColumn: 1,
            type: "string",
            role: "annotation"
        },
        2
    ]);

    var options = {
        width: 400,
        height: 220,
        bar: {groupWidth: "95%"},
        legend: {
            textStyle: {
                color: 'white',
            }
        },
        titleTextStyle: {
            color: 'white',
        },
        legend: { position: "none" },
        backgroundColor: 'none',
        fontName: 'Turret Road',
        hAxis: {
            textStyle: {
                color: 'white'
            }
        },
        vAxis: {
            textStyle: {
                color: 'white'
            }
        },
        chartArea: {
            textStyle: {
                color: 'white'
            }
        }
    };

    var chart = new google.visualization.ColumnChart(chartDiv);
    chart.draw(view, options);

}

function setData(container, data) {
    const nickname = container.querySelector('.list-nickname');
    nickname.textContent = data.nickname;

    const userPhoto = container.querySelector('.list-user-photo');
    userPhoto.src = `http://localhost:8003/${data.photo}`;

    const scores = container.querySelector('.list-scores');
    scores.textContent = data.scores;

    const userPlaying = container.querySelector('.list-user-game-status');

    const icon = document.createElement('i');
    icon.classList.add('fa-solid', 'fa-circle', 'me-2', 'mt-2');
    let colorPlaying = 'white';
    let textPlaying = 'Offline';
    if (data.status) {
        if (data.playing) {
            colorPlaying = 'red';
            textPlaying = 'In Game';
        }
        else {
            colorPlaying = 'green';
            textPlaying = 'Free';
        }
    }
    icon.style.color = colorPlaying;
    userPlaying.appendChild(icon);

    const labelPlaying = document.createElement('strong');
    labelPlaying.textContent = textPlaying;
    userPlaying.appendChild(labelPlaying);
}

function createMainContainer() {
    const container = document.createElement('div');
    container.classList.add('container');
    return container;
}

function createRow(container){
    const row = document.createElement('div');
    row.classList.add('row', 'row-item-list', 'd-flex', 'align-items-center', 'mb-3');
    container.appendChild(row);
    return row;
}


function createCol1(){
    const col1 = document.createElement('div');
    col1.classList.add('col-2');
    return col1;
}

function createUserPhoto(data) {
    const userPhoto = document.createElement('img');
    const detailsInfosUser = document.getElementById('details-infos-user');
    const detailsMedalUser = document.getElementById('details-medal-user');
    const detailsPhotoUser = document.getElementById('details-photo-user');
    userPhoto.classList.add('list-user-photo');

    let oldValuesUser = ``;
    let oldMedalUser = ``;
    let oldPhotoUser = ``;
    userPhoto.addEventListener('mouseover', function() {
        oldValuesUser = document.getElementById('details-infos-user').innerHTML;
        oldMedalUser = document.getElementById('details-medal-user').innerHTML;
        oldPhotoUser = document.getElementById('details-photo-user').innerHTML;
        gameInfoService.get_user(data.id).then(
            res => {
                setDetailsStatus(res);
                drawChart(detailsInfosUser, res);
                drawChartMedalRaking(detailsMedalUser, res);
            }
        );
    });
    userPhoto.addEventListener('mouseleave', function() {
        detailsInfosUser.innerHTML = oldValuesUser;
        detailsMedalUser.innerHTML = oldMedalUser;
        detailsPhotoUser.innerHTML = oldPhotoUser;
    });

    return userPhoto;
}

function createCol2() {
    const col2 = document.createElement('div');
    col2.classList.add('col-5');
    return col2;
}

function createNickName () {
    const nickname = document.createElement('p');
    nickname.classList.add('list-nickname', 'p-3', 'shadow');
    return nickname;
}

function createCol3() {
    const col3 = document.createElement('div');
    col3.classList.add('col-3');
    return col3;
}

function createScores(){
    const scores = document.createElement('p');
    scores.classList.add('list-scores', 'p-3', 'shadow');
    return scores;
}

function createCol4 () {
    const col4 = document.createElement('div');
    col4.classList.add('col-2');
    return col4;
}

function createUserGameStatus() {
    const userGameStatus = document.createElement('p');
    userGameStatus.classList.add('list-user-game-status', 'p-3', 'shadow');
    return userGameStatus;
}

function setDetailsStatus(data) {
    document.getElementById('details-fullname').textContent = data.user.full_name;
    document.getElementById('details-nickname').textContent = data.user.nickname;
    document.getElementById('details-scores').textContent = data.user.scores;
    document.getElementById('details-winnings').textContent = data.user.winnings;
    document.getElementById('details-losses').textContent = data.user.losses;
    document.getElementById('details-position').textContent = `${data.user.position}º`;
    document.getElementById('details-photo').src = `http://localhost:8003/${data.user.photo}`;
    document.getElementById('details-status-icon').style.color = data.user.status ? 'green' : 'white';
    document.getElementById('details-status-label').textContent = data.user.status ? 'Online' : 'Offline';
}

function AddUserInList(data) {
    let containers = document.getElementById('containers');

    const container = createMainContainer();
    containers.appendChild(container);

    const row = createRow(container);
    const col1 = createCol1();
    row.appendChild(col1);
    const userPhoto = createUserPhoto(data);
    col1.appendChild(userPhoto);
    const col2 = createCol2();
    row.appendChild(col2);
    const nickname = createNickName();
    col2.appendChild(nickname);
    const col3 = createCol3();
    row.appendChild(col3);
    const scores = createScores();
    col3.appendChild(scores);
    const col4 = createCol4();
    row.appendChild(col4);
    const userGameStatus = createUserGameStatus();
    col4.appendChild(userGameStatus);
    setData(container, data);
    container.addEventListener('click', function() {
        gameInfoService.get_user(data.id).then(
            res => {
                setDetailsStatus(res);
            }
        );
    });

}

const start = () => {
    gameInfoService.gameInfo().then(
      res => {
        res.forEach(data => {
            AddUserInList(data);
        });
    });

    gameInfoService.totalInfos().then(
        res => {
            const totalScores = document.getElementById('total_scores');
            totalScores.textContent = res.total_scores;

            const totalPlayers = document.getElementById('total_players');
            totalPlayers.textContent = res.total_players;
    });
}

export default new GameInfoView(html, start);
