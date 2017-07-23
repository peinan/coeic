'use strict';

if (process.argv.length < 3) {
  throw Error("Usage: " + process.argv.join(" ") + " <storage_root_path>")
}

// 実際に保存されるストレージのルート
const storage_root = process.argv[2].endsWith("/") ? process.argv[2] : process.argv[2] + "/";

// それぞれの相対パス
const uploaded_img_relative_path = "uploaded_imgs/";
const processed_img_relative_path = "processed_imgs/";
const voice_relative_path = "voices/";

// それぞれの保存先
const uploaded_img_root = storage_root + uploaded_img_relative_path;
const processed_img_root = storage_root + processed_img_relative_path;
const voice_root = storage_root + voice_relative_path;

// APIのベースURL
const base_url = "http://104.155.222.216:5000/";

// 実際の画像にアクセスするためのURL
const uploaded_img_path_url = base_url + uploaded_img_relative_path;
const processed_img_path_url = base_url + processed_img_relative_path;
const voice_path_url = base_url + voice_relative_path;

const express = require('express');
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const server = app.listen(5000, function () {
  console.log("Node.js is listening to PORT:" + server.address().port);
});

const db = require('./db');

const multer = require('multer');
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploaded_img_root);
  },
  filename: function (req, file, cb) {
    cb(null, new Date().getTime() + ".jpg");
  }
});
const upload = multer({storage: storage});

/**
 * upload image
 * https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_POST:uploadedImg
 */
app.post("/api/uploadedImg", upload.single('file'), function (req, res) {
  const walkSync = require('walk-sync');

  try {
    // 最新の画像ファイル名を取得
    const filename =
      Math.max.apply(null, walkSync(uploaded_img_root).map(function (name, index, array) {
      return name.split(".")[0];
    })).toString() + '.jpg';

    // DBにデータ追加
    db.insert(filename, db.STATUS_TODO, '').then(function (results) {
      // 追加した最新のデータを返す
      db.selectMulti(1).then(function (results) {
        const result = results[0];
        res.send({
          status: "success",
          result: {
            id: result.id,
            url: uploaded_img_path_url + result.filename,
            status: result.status,
            created_at: result.created_at,
            updated_at: result.updated_at
          }
        })
      }).catch(function (err) {
        throw err;
      })
    }).catch(function (err) {
      throw err;
    });

  } catch (e) {
    console.log(e);
    res.send({
      status: "failure",
      result: {
        message: "画像のアップロードに失敗しました"
      }
    });
  }
});


/**
 * get all of uploaded images
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:uploadedImg">wiki</a>
 */
app.get("/api/uploadedImg", function (req, res) {
  try {
    const results = typeof req.body["results"] !== 'undefined' ? req.body["results"] : 0;

    // body.resultsが未指定または0の場合は全ての画像を取得（とはいえ上限を設けておく）
    const max_num = results === 0 ? 65535 : results;

    // DBから画像情報取得
    db.selectMulti(max_num).then(function (results) {
      const info_list = results.map(function (r) {
        return {
          id: r.id,
          url: uploaded_img_path_url + r.filename,
          status: r.status,
          created_at: r.created_at,
          updated_at: r.updated_at
        }
      });
      res.send({
        status: "success",
        result: info_list
      })
    }).catch(function (err) {
      throw err;
    });
  } catch (e) {
    console.log(e);
    res.send({
      status: "failure",
      result: {
        message: "画像取得に失敗しました"
      }
    });
  }
});

/**
 * get the specified uploaded image
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:uploadedImg">wiki</a>
 */
app.get("/api/uploadedImg/:id", function (req, res, next) {
  try {
    // DBから画像情報取得
    db.select(req.params.id).then(function (results) {
      const info_list = results.map(function (r) {
        return {
          id: r.id,
          url: uploaded_img_path_url + r.filename,
          status: r.status,
          created_at: r.created_at,
          updated_at: r.updated_at
        }
      });
      if (info_list.length === 0) {
        res.send({
          status: "failure",
          result: {
            message: "画像が存在しません"
          }
        });
        next();
      }
      res.send({
        status: "success",
        result: info_list[0]
      })
    }).catch(function (err) {
      throw err;
    });
  } catch (e) {
    console.log(e);
    res.send({
      status: "failure",
      result: {
        message: "画像取得に失敗しました"
      }
    });
  }
});

/**
 * find processed images
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:processedImg">wiki</a>
 */
app.get("/api/processedImg/:id", function (req, res) {

  const walkSync = require('walk-sync');

  var result;

  try {
    var paths = walkSync(processed_img_root + req.params.id);
    paths = paths.map(function (name) {
      return processed_img_path_url + req.params.id + "/" + name;
    });
    result = {
      status: "success",
      result: paths
    }
  } catch (e) {
    result = {
      status: "failure",
      result: {
        message: "画像取得に失敗しました",
        cause: e
      }
    }
  }

  res.send(result);
});

/**
 * get the processed image
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:processedImg">wiki</a>
 */
app.get(processed_img_relative_path + ":id/:name", function (req, res) {

  const fileExists = require('file-exists');

  const options = {
    root: processed_img_root + req.params.id + "/"
  };

  const filename = req.params.name;

  fileExists(filename, options, function (err, exists) {
    if (!err && exists) {
      res.sendFile(filename, options);
    } else {
      res.send({
        status: "failure",
        result: {
          message: "画像取得に失敗しました"
        }
      });
    }
  });
});

/**
 * find voice files
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:voice">wiki</a>
 */
app.get("/api/voice/:id", function (req, res) {

  const walkSync = require('walk-sync');

  var result;

  try {
    var paths = walkSync(voice_root + req.params.id);
    paths = paths.map(function (name) {
      return voice_path_url + req.params.id + "/" + name;
    });
    result = {
      status: "success",
      result: paths
    }
  } catch (e) {
    result = {
      status: "failure",
      result: {
        message: "音声取得に失敗しました",
        cause: e
      }
    }
  }

  res.send(result);
});

/**
 * get the voice file
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:voice">wiki</a>
 */
app.get(voice_relative_path + ":id/:name", function (req, res) {

  const fileExists = require('file-exists');

  const options = {
    root: voice_root + req.params.id + "/"
  };

  const filename = req.params.name;

  fileExists(filename, options, function (err, exists) {
    if (!err && exists) {
      res.sendFile(filename, options);
    } else {
      res.send({
        status: "failure",
        result: {
          message: "音声取得に失敗しました"
        }
      });
    }
  });
});