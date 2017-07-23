'use strict';

if (process.argv.length < 3) {
  throw Error("Usage: " + process.argv.join(" ") + " <storage_root_path>")
}

const db = require('./db');

// 実際に保存されるストレージのルート
const storage_root = process.argv[2].endsWith("/") ? process.argv[2] : process.argv[2] + "/";

// 一時保存ディレクトリ名
const tmp_dir = storage_root + Date.now().toString() + '/';
const mkdirp = require('mkdirp');
const rmdir = require('rmdir');

// APIのベースURL
const base_url = "http://104.155.222.216:5000/";

const express = require('express');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
/**
 * Cross-Origin Resource Sharingを有効にする記述（HTTPレスポンスヘッダの追加）
 */
app.use(function (req, res, next) {
  res.header('Access-Control-Allow-Origin', req.headers.origin);
  res.header('Access-Control-Allow-Headers', 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept, Cache-Control');
  res.header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Credentials', true);
  res.header('Access-Control-Max-Age', '86400');
  next();
});
app.use((req, res, next) => {
  mkdirp(tmp_dir, (e) => {
    if (e) console.log(e);
  });
  next();
});

/**
 * OPTIONSメソッドの実装
 */
app.options('*', function (req, res) {
  res.sendStatus(200);
});

const server = app.listen(5000, function () {
  console.log("Node.js is listening to PORT:" + server.address().port);
});

const multer = require('multer');
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, tmp_dir);
  },
  filename: function (req, file, cb) {
    const path = require('path');
    const ext = path.extname(file.originalname);
    cb(null, 'original' + ext);
  }
});
const upload = multer({storage: storage});

/**
 * 返送用メッセージ作成
 * @param status  'success' or 'failure'
 * @param message message
 * @returns {{status: *, result: {message: *}}}
 */
function createMessage(status, message) {
  return {
    status: status,
    result: {
      message: message
    }
  }
}

/**
 * upload image
 * https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_POST:uploadedImg
 */
app.post("/api/uploadedImg", upload.single('file'), function (req, res) {

  const walkSync = require('walk-sync');
  const path = require('path');

  try {
    // filename取得
    const filename = walkSync(tmp_dir).filter((name) => name.startsWith('original'))[0];
    // まずDBに追加
    db.insert(filename, db.STATUS_DOING, '').then(() => {
      // DBからID取得
      db.selectMulti(1).then((results) => {
        const result = results[0];
        const id_dir = storage_root + result.id;
        // すでにid名のディレクトリがある場合は削除
        const directoryExists = require('directory-exists');
        if (directoryExists.sync(id_dir)) {
          rmdir(id_dir, (err) => {
            if (err) console.log(err);
          })
        }
        // 一時保存ディレクトリをid名に移動
        const mv = require('mv');
        mv(tmp_dir, id_dir, {mkdirp: true},  (err) => {
          if (err) {
            console.log(err);
            res.send(createMessage('failure', 'ディレクトリの移動に失敗'))
          } else {
            // DB情報を更新
            db.update(result.id, db.STATUS_TODO, '').then(() => {
              // 追加した最新のデータを返す
              res.send({
                status: "success",
                result: {
                  id: result.id,
                  url: base_url + result.id + "/" + filename,
                  status: db.STATUS_TODO,
                  created_at: result.created_at,
                  updated_at: result.updated_at
                }
              })
            }).catch((e) => {
              console.log(e);
              res.send(createMessage('failure', 'DBの初回情報更新に失敗'))
            });
          }
        });
      }).catch((e) => {
        console.log(e);
        res.send(createMessage('failure', 'DBからの最新情報取得に失敗'))
      })
    }).catch((e) => {
      console.log(e);
      res.send(createMessage('failure', 'DBへの初回登録に失敗'))
    });
  } catch (e) {
    console.log(e);
    res.send(createMessage('failure', '画像のアップロードに失敗'))
  }
});

/**
 * get all of uploaded images info
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:uploadedImg">wiki</a>
 */
app.get("/api/uploadedImg", function (req, res) {
  try {
    const param = typeof req.body["results"] !== 'undefined' ? req.body["results"] : 0;

    // body.resultsが未指定または0の場合は全ての画像を取得（とはいえ上限を設けておく）
    const max_num = param === 0 ? 65535 : param;

    // DBから画像情報取得
    db.selectMulti(max_num).then((results) => {
      const info_list = results.map((r) => {
        return {
          id: r.id,
          url: base_url + r.id + "/" + r.filename,
          status: r.status,
          created_at: r.created_at,
          updated_at: r.updated_at
        }
      });
      res.send({
        status: "success",
        result: info_list
      })
    }).catch((e) => {
      console.log(e);
      res.send(createMessage('failure', 'DBからの画像情報取得に失敗'))
    });
  } catch (e) {
    console.log(e);
    res.send(createMessage('failure', '画像情報取得に失敗'))
  }
});

/**
 * get the specified uploaded image info
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:uploadedImg">wiki</a>
 */
app.get("/api/uploadedImg/:id", function (req, res) {
  try {
    // DBから画像情報取得
    db.selectById(req.params.id).then((results) => {
      const info_list = results.map(function (r) {
        return {
          id: r.id,
          url: base_url + r.id + "/" + r.filename,
          status: r.status,
          created_at: r.created_at,
          updated_at: r.updated_at
        }
      });
      if (info_list.length === 0) {
        res.send(createMessage('failure', 'DBに画像情報が存在しません'))
      } else {
        res.send({
          status: "success",
          result: info_list[0]
        })
      }
    }).catch((e) => {
      console.log(e);
      res.send(createMessage('failure', 'DBからの画像情報取得に失敗'))
    });
  } catch (e) {
    console.log(e);
    res.send(createMessage('failure', '画像情報取得に失敗'))
  }
});

/**
 * get the specified uploaded image data
 */
app.get("/:id/:name", function (req, res) {
  const fileExists = require('file-exists');

  const options = {
    root: storage_root + req.params.id
  };

  const filename = req.params.name;

  fileExists(filename, options, (err, exists) => {
    if (!err && exists) {
      res.sendFile(filename, options);
    } else {
      console.log(err);
      res.send(createMessage('failure', '画像取得失敗'));
    }
  });
});

/**
 * find processed images
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:processedImg">wiki</a>
 */
app.get("/api/processedImg/:id", function (req, res) {
  // DBから指定されたidのmessageを取得してDONEであればjsonとみなしてパース
  const id = req.params.id;
  db.selectById(id).then((results) => {
    if (results.length !== 0 && results[0].status === db.STATUS_DONE) {
      const result = results[0];
      const message = result.message;
      const data = JSON.parse(message);
      const processed_img_urls = data.splitted_frames.map((f) => {
        return base_url + id + '/frames/' + f.frame_img;
      });
      res.send({
        status: 'success',
        result: processed_img_urls
      });
    } else {
      res.send('failure', "指定されたidの処理済み画像はありません: " + id);
    }
  }).catch((e) => {
    console.log(e);
    res.send('failure', '画像取得に失敗しました');
  });
});

/**
 * get the processed image
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:processedImg">wiki</a>
 */
app.get("/:id/frames/:name", function (req, res) {
  const fileExists = require('file-exists');

  const options = {
    root: storage_root + req.params.id + "/frames/"
  };

  const filename = req.params.name;

  fileExists(filename, options, function (err, exists) {
    if (!err && exists) {
      res.sendFile(filename, options);
    } else {
      res.send('failure', '処理画像取得に失敗しました');
    }
  });
});

/**
 * find voice files
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:voice">wiki</a>
 */
app.get("/api/voice/:id", function (req, res) {

  const flatten = require('flatten');

  const id = req.params.id;
  db.selectById(id).then((results) => {
    if (results.length !== 0 && results[0].status === db.STATUS_DONE) {
      const result = results[0];
      const message = result.message;
      const data = JSON.parse(message);
      const voice_urls = data.splitted_frames.map((f) => {
        return f.extracted_balloons.map((b) => {
          return base_url + id + "/voice/" + b.texts.speech;
        });
      });
      res.send({
        status: 'success',
        result: flatten(voice_urls)
      });
    } else {
      res.send('failure', "指定されたidの音声はありません: " + id);
    }
  }).catch((e) => {
    console.log(e);
    res.send('failure', '音声取得に失敗しました');
  });
});

/**
 * get the voice file
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:voice">wiki</a>
 */
app.get("/:id/voice/:name", function (req, res) {

  const fileExists = require('file-exists');

  const options = {
    root: storage_root + req.params.id + "/voice/"
  };

  const filename = req.params.name;

  fileExists(filename, options, function (err, exists) {
    if (!err && exists) {
      res.sendFile(filename, options);
    } else {
      res.send('failure', '音声取得に失敗しました');
    }
  });
});

/**
 * テーブルの要素を全て削除する
 */
app.get("/api/truncate", function (req, res) {
  db.truncate().then(function () {
    const message = 'succeeded to truncate table';
    console.log(message);
    res.send('success', message);
  }).catch(function (e) {
    console.log(e);
    res.send('failure', 'failed to truncate table: ' + e);
  })
});