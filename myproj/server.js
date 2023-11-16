var express = require('express');
var bodyParser = require('body-parser');
var mysql = require('mysql2');
var path = require('path');
var connection = mysql.createConnection({
  host: '146.148.85.94',
  user: 'root',
  password: 'team004',
  database: 'classicmodels'
});

const userIDMap = new Map();
const passwordArr = [];
connection.connect;


var app = express();
var mainID = 0;
// set up ejs view engine 
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(__dirname + '../public'));

/* GET home page, respond by rendering index.ejs */
app.get('/', function (req, res) {
  res.render('login');
});

app.get('/sign_in', function (req, res) {
  res.render('index');
});

app.get('/success', function (req, res) {
  //render the page with advanced queries
  res.render('advanced', { ratings: '', userNames: '', data: '', data1: '', data2: '' });
  // res.render('advanced', {data1: ''});
  // res.render('advanced', {data2: ''});
});

app.post('/login', function (req, res) {
  var userName = req.body.username;
  var password = req.body.password;
  var login_success = 0;
  var sql = `SELECT UserID, UserName, Password FROM User WHERE UserName LIKE '%${userName}%' AND Password LIKE '%${password}%'`;

  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    if (result.length == 1) {
      login_success = 1;
      mainID = result[0].UserID;
      // console.log(`mainID: ${result}`)
      console.log(result[0].UserID);
    }
    else {
      login_success = 0;
    }
    if (login_success) {
      res.redirect('/success');
    }
    else {
      res.redirect('/');
    }
  });
});

app.post('/create_account', function (req, res) {
  res.redirect('/sign_in');
});

// this code is executed when a user clicks the form submit button
app.post('/mark', function (req, res) {
  var email = req.body.email;
  var userName = req.body.userName;
  var password = req.body.password;
  var minm = 10000;
  var maxm = 99999;
  var UserID = Math.floor(Math
    .random() * (maxm - minm + 1)) + minm;
  //to make sure two users don't have the same userID
  while (userIDMap.has(UserID)) {
    UserID = Math.floor(Math
      .random() * (maxm - minm + 1)) + minm;
  }
  mainID = UserID;
  //we still have to check for duplicate usernames
  userIDMap.set(UserID, userName);
  // passwordMap.set(userName, password);
  // passwordArr.push([userName, password]);
  var sql = `INSERT INTO User (UserID, Email, Password, UserName) VALUES ('${UserID}','${email}','${password}','${userName}')`;
  // make the userIDd global var for access
  mainID = UserID;
  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    res.redirect('/success');
  });
});

app.post('/search', function (req, res) {
  var gameName = req.body.gameName;

  var sql = `SELECT Name, ID FROM Game WHERE Name LIKE '%${gameName}%' ORDER BY Name, ID LIMIT 15`;

  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    var obj = { advanced: result };
    res.render('advanced', { ratings: '', userNames: '', data: result, data1: '', data2: '' });
  });
});


app.post('/update', function (req, res) {
  var gameID = req.body.gameID;
  var newValue = req.body.gameVal;

  var sql = `
    UPDATE Game
    SET MetaCritic = ${newValue}
    WHERE ID= ${gameID}
  `;

  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err);
      return;
    }
    res.redirect('/success');
  });
});

app.post('/delete', function (req, res) {
  var userName = req.body.userName;
  var sql = `DELETE FROM User WHERE UserName = '${userName}'`;

  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err);
      return;
    }
    res.redirect('/success');
  });
});


app.post('/advanced1', function (req, res) {

  var sql = `SELECT Name, FinalPrice, MetaCritic FROM Game WHERE 
FinalPrice >= (SELECT AVG(FinalPrice) FROM Game WHERE DLCcount > 1)
INTERSECT
SELECT Name, FinalPrice, MetaCritic FROM Game WHERE 
MetaCritic >= (SELECT AVG(MetaCritic) FROM Game WHERE DeveloperCount > 1)
ORDER BY MetaCritic DESC, Name LIMIT 15`;

  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    var obj = { advanced: result };
    res.render('advanced', { ratings: '', userNames: '', data1: result, data: '', data2: '' });
  });
});

app.post('/advanced2', function (req, res) {

  var sql = `SELECT g.Name, g.MetaCritic FROM Game g JOIN Features f ON (g.ID = f.GameID)
WHERE f.FREE = TRUE AND g.MetaCritic >= (SELECT AVG(g1.MetaCritic) FROM Game g1 JOIN Features f1
ON (g1.ID = f1.GameID) WHERE f1.Free = TRUE)
ORDER BY MetaCritic DESC, Name LIMIT 15`;

  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    var obj = { advanced: result };
    res.render('advanced', { ratings: '', userNames: '', data2: result, data: '', data1: '' });
  });
});

app.post('/searchFriend', function (req, res) {
  var userName = req.body.userName;

  var sql = `SELECT UserName, UserID, FriendCount
               FROM User
               WHERE UserName LIKE '%${userName}%'
               ORDER BY UserName, UserID
               LIMIT 30
               `;

  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    res.render('advanced', { ratings: '', userNames: result, data: '', data1: '', data2: '' }); // CHANGE: I am not too sure if i should add another data variable that holds the result
  });
});

app.post('/addFriend', function (req, res) {
  var friendID = req.body.userID;
  var date = new Date();
  let dateStr = '8/3/23';
  var sql = `INSERT INTO FriendList VALUES (${friendID}, ${mainID}, ${dateStr})`;

  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    res.redirect('/success');
  });
});

app.post('/rateGame', function (req, res) {
  var sql = `CALL gameGenreCompare()`;
  console.log(sql);
  connection.query(sql, function (err, result) {
    if (err) {
      res.send(err)
      return;
    }
    res.render('advanced', { ratings: result[0], userNames: '', data2: '', data: '', data1: '' })
  });
});

app.post('/genre', function (req, res) {
  res.render('Genreinteractive')
});

app.post('/actionsales', function (req, res) {
  res.render('ActionSales')
});

app.post('/cod', function (req, res) {
  res.render('CallOfDuty')
});

app.post('/actionKeyword', function (req, res) {
  res.render('ActionKeywords')
});


app.listen(80, function () {
  console.log('Node app is running on port 80');
});










