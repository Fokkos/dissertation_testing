// finds the winner of the election and updates the modal with the winner(s)
function findWinner() {
    if (checkResultsValidation()) {
        
        // clear the winnersDiv
        document.querySelector('.winnersDiv').innerHTML = '';

        // get the Winner of the election
        getWinner()

        // open the modal
        openModal('winnerModal');

        // confetti
        confetti({
        particleCount: 500,
        spread: 100
        });
    }
}

// calls a function to the backend to get the winner of the election
// and updates the modal with the winner(s)
function getWinner() {
    const url = "/getWinner"
    fetch(url)
    .then(response => response.json())  
    .then(json => {
        if (json['election_type'] == 'single-winner') {
            document.getElementById('winnerDivTitleText').innerText = 'Winner:';
            createIndividualText(0, json['winner'], json['voting_style'], json['election_type']);
        } else {
            document.getElementById('winnerDivTitleText').innerText = 'Winners:';
            for (winner in json['winner'].slice(0, 10)) {
                createIndividualText(winner, json['winner'][winner], json['voting_style'], json['election_type']);
            }
            if (json['election_type'] == 'participatory-budget') {
                if (!json['winners']) { // if no winner are found (only vote is above budget)
                    let winnerDiv = document.createElement('div');
                    winnerDiv.className = 'flex justify-center pt-3 px-10 text-3xl font-bold';
                    let winnerText = document.createTextNode('No winners found');
                    winnerDiv.appendChild(winnerText);
                    document.querySelector('.winnersDiv').appendChild(winnerDiv);

                    let infoDiv = document.createElement('div');
                    infoDiv.className = 'flex justify-center pt-3 px-10 text-xl font-bold';
                    let infoText = document.createTextNode('All votes made were above the allocated budget.');
                    infoDiv.appendChild(infoText);
                    document.querySelector('.winnersDiv').appendChild(infoDiv);
                    
                } else {
                    let winnerDiv = document.createElement('div');
                    winnerDiv.className = 'flex justify-center pt-3 px-10 text-sm font-bold';
                    let winnerText = document.createTextNode('Remaining Budget: ' + json['remaining_budget']);
                    winnerDiv.appendChild(winnerText);
                    document.querySelector('.winnersDiv').appendChild(winnerDiv);

                    if (json['winner'].length > 10) {
                        let winnerDiv = document.createElement('div');
                        winnerDiv.className = 'flex justify-center pt-3 px-10 text-sm font-bold';
                        let winnerLink = document.createElement('a');
                        winnerLink.href = "/winners";
                        winnerLink.innerText = 'Too many winners to display, click here to see all winners.';
                        winnerDiv.appendChild(winnerLink);
                        document.querySelector('.winnersDiv').appendChild(winnerDiv);
                    }
                }
            }
        }
    })
}

// depending on what position a candidate got, the text size will be different
// this function returns the tailwindCSS classes for the text size
function getTextSize(position){
    if (position == 0){
        return ['text-3xl'];
    } else if (position == 1){
        return ['text-2xl'];
    } else if (position == 2){
        return ['text-xl'];
    } else {
        return ['text-lg'];
    }
}

// returns the score type based on the voting style
function getScoreType(voting_style) {
    if (voting_style == 'average-voter') {
        return 'Distance: ';
    }
    if (voting_style == 'ranked-choice') {
        return 'Borda Score: ';
    }
    if (voting_style == 'plurality') {
        return 'Votes: ';
    }
}

// creates a div with the winner name and score and appends it to the winnersDiv
function createIndividualText(position, winner, voting_style, election_type) {
    const winnerDiv = document.createElement('div');
    //give winnerDiv a class
    winnerDiv.className = 'flex justify-center py-0 px-10 font-bold';
    // get the text size of the current position and add it to the winnerDiv
    // spread operator to add multiple classes (...list)
    winnerDiv.classList.add(...getTextSize(position));
    //create a text node with the winner name
    const winnerText = document.createTextNode('#' + (parseInt(position)+1) + ': ' + winner[0]);
    //append the text node to the winnerDiv
    winnerDiv.appendChild(winnerText);
    //append the winnerDiv to the winnersDiv
    document.querySelector('.winnersDiv').appendChild(winnerDiv);

    scoreDiv = document.createElement('div');
    scoreDiv.className = 'flex justify-center py-0 px-10 text-sm';
    let scoreText = (getScoreType(voting_style) + Math.round(parseFloat(winner[1]) * 100) / 100);
    if (election_type == 'participatory-budget') {
        scoreText += (",   Cost: " + winner[2]);
    }
    scoreText = document.createTextNode(scoreText);
    scoreDiv.appendChild(scoreText);
    document.querySelector('.winnersDiv').appendChild(scoreDiv);
}