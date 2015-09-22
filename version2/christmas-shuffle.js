var elements = [];
// var elements = [
//   {
//     firstName: "person1FirstName",
//     lastName: "person1LastName"
//   },
//   {
//     firstName: "person2FirstName",
//     lastName: "person2LastName"
//   }
// ];

$(document).ready(function () {
  for (i = 0; i < elements.length; i++) {
    updatePersonList({
      firstName: elements[i].firstName,
      lastName: elements[i].lastName
    });
  }
  $(".shuffle").on("click", function(e) { shuffle(); });
  $(".addElement").on("click", function(e) { addElement(retrieveNewElement()); });
});

function retrieveNewElement() {
  var newPerson = {};
  newPerson["firstName"] = $(".firstName").val();
  newPerson["lastName"] = $(".lastName").val();
  return newPerson;
}

function isNewElement(proposedNewElement) {
  for (i = 0; i < elements.length; i++) {
    if(proposedNewElement.firstName == elements[i].firstName && proposedNewElement.lastName == elements[i].lastName) {
      return false;
    }
  }
  return true;
}

function updatePersonList(newPerson) {
  $(".personList").append("<li>" + newPerson.firstName + " " + newPerson.lastName + "</li>");
}

function addElement(newPerson) {
  if(isNewElement(newPerson)) {
    elements.push(newPerson);
    updatePersonList(newPerson);
  } else {
    alert("The current entry cannot be accepted. All elements in the list must be unique.");
  }
}

function organizePeople(everyone) {
  people = {}
  for(i = 0; i < everyone.length; i++) {
    if(everyone[i].lastName in people) {
      people[everyone[i].lastName].push(everyone[i].firstName);
    } else {
      people[everyone[i].lastName] = [everyone[i].firstName];
    }
  }

  return people;
}

function updateShuffledListShown(person) {
  $(".shuffledList").append("<li>" + person.firstName + " " + person.lastName + " gives to " + person.givesToFirstName + " " + person.givesToLastName + "</li>");
}

function updateGivesToList(everyone) {
  for(i = 0; i < everyone.length; i++) {
    updateShuffledListShown(everyone[i]);
  }
}

function canGiveToList(notReceivedPeople, lastName) {
  var nonFamily = $.extend({}, people);
  delete nonFamily[lastName];
  return nonFamily;
}

function generateRandomNumber(belowThisNumber) {
  return Math.floor(Math.random() * belowThisNumber);
}

function deepCopy() {
  var allElements = {};
  for(i = 0; i < elements.length; i++) {
    allElements.push({
      firstName: elements[i].firstName,
      lastName: elements[i].lastName,
    })
  }
}

function shuffle() {
  $(".shuffledList").empty();

  runAgain = true;
  while(runAgain) {
    runAgain = false;

    var giving = $.extend([], elements);
    var givingPeople = organizePeople(giving);
    var notReceivedPeople = organizePeople(giving);

    if(Object.keys(notReceivedPeople).length == 1) {
      console.log("cannot shuffle without at least two families...");
      break;
    }

    for (var lastName in givingPeople) {
      for (i = 0; i < givingPeople[lastName].length; i++) {
        var firstName = givingPeople[lastName][i];

        canGiveTo = canGiveToList(notReceivedPeople, lastName);

        var lastNameArray = Object.keys(canGiveTo);
        if(lastNameArray.length == 0) {
          console.log("random choices are seldom ideal... starting over");
          runAgain = true;
          break;
        }
        var randomLastNameIndex = (generateRandomNumber(lastNameArray.length) + generateRandomNumber(lastNameArray.length)) % lastNameArray.length;
        var givesToLastName = lastNameArray[randomLastNameIndex];

        var firstNameArray = canGiveTo[givesToLastName];
        var randomFirstNameIndex = (generateRandomNumber(firstNameArray.length) + generateRandomNumber(firstNameArray.length)) % firstNameArray.length;
        var givesToFirstName = firstNameArray[randomFirstNameIndex];

        if(notReceivedPeople[givesToLastName].length == 1) {
          delete notReceivedPeople[givesToLastName];
        } else {
          notReceivedPeople[givesToLastName].splice(randomFirstNameIndex, 1);
        }

        for(j = 0; j < giving.length; j++) {
          if(giving[j].firstName == firstName && giving[j].lastName == lastName) {
            giving[j]["givesToFirstName"] = givesToFirstName;
            giving[j]["givesToLastName"] = givesToLastName;
            break;
          }
        }
      }
      if(runAgain) {
        break;
      }
    }
  }
  updateGivesToList(giving);
}
