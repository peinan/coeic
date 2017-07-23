'use strict';

if (process.argv.length < 3) {
  throw Error("Usage: " + process.argv.join(" ") + " <storage_root_path>")
}

const storage_root = process.argv[2].endsWith("/") ? process.argv[2] : process.argv[2] + "/";
const upload_img_root = storage_root + "uploaded_imgs/";
const img_root = storage_root + "processed_imgs/";
const voice_root = storage_root + "voice/";

const base_url = "http://104.155.222.216:5000/api/";
const upload_img_url = base_url + "uploadedImg/";
const img_url = base_url + "processedImg/";
const voice_url = base_url + "voice/";

const express = require("express");
const app = express();
const bodyParser = require('body-parser');

app.use(bodyParser.json());

const server = app.listen(5000, function () {
  console.log("Node.js is listening to PORT:" + server.address().port);
});

/** get all of uploaded images
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:uploadedImg">wiki</a>
 */
app.get("/api/uploadedImg", function (req, res) {
  const walkSync = require('walk-sync');
  const fs = require('fs');

  var result;

  try {
    const results = typeof req.body["results"] !== 'undefined' ? req.body["results"] : 0;

    // body.resultsが未指定または0の場合は全ての画像を取得（とはいえ上限を設けておく）
    const max_num = results === 0 ? 65535 : results;

    var paths = walkSync(upload_img_root);
    paths = paths.slice(0, max_num + 1);
    const info_list = paths.map(function (name, index, array) {
      // todo:  DBからファイル情報取得．今はダミー実装
      const stat = fs.statSync(upload_img_root + name);
      return {
        id: parseInt(name.split(".")[0]),
        url: upload_img_url + name,
        status: "done",
        created_at: stat.birthtime,
        updated_at: stat.ctime
      };
    });

    result = {
      status: "success",
      result: info_list
    }

  } catch (e) {
    result = {
      status: "failure",
      result: {
        message: "画像取得に失敗しました"
      }
    }
  }

  res.send(result);
});

/** get the specified uploaded image
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:uploadedImg">wiki</a>
 */
app.get("/api/uploadedImg/:id", function (req, res) {

  const walkSync = require('walk-sync');
  const fs = require('fs');

  var result;

  try {
    var paths = walkSync(upload_img_root);
    const info_list = paths.filter(function (name) {
      return parseInt(name.split(".")[0]) === parseInt(req.params.id);
    }).map(function (name, index, array) {
      // todo:  DBからファイル情報取得．今はダミー実装
      const stat = fs.statSync(upload_img_root + name);
      return {
        id: parseInt(name.split("/")[0]),
        url: upload_img_url + name,
        status: "done",
        created_at: stat.birthtime,
        updated_at: stat.ctime
      };
    });

    if (info_list.length === 0) {
      throw Error();
    }
    const info = info_list[0];

    result = {
      status: "success",
      result: info
    }

  } catch (e) {
    result = {
      status: "failure",
      result: {
        message: "画像取得に失敗しました"
      }
    }
  }

  res.send(result);
});

/** find processed images
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:processedImg">wiki</a>
 */
app.get("/api/processedImg/:id", function (req, res) {

  const walkSync = require('walk-sync');

  var result;

  try {
    var paths = walkSync(img_root + req.params.id);
    paths = paths.map(function (name) {
      return img_url + req.params.id + "/" + name;
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

/** get the processed image
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:processedImg">wiki</a>
 */
app.get("/api/processedImg/:id/:name", function (req, res) {

  const fileExists = require('file-exists');

  const options = {
    root: img_root + req.params.id + "/"
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

/** find voice files
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:voice">wiki</a>
 */
app.get("/api/voice/:id", function (req, res) {

  const walkSync = require('walk-sync');

  var result;

  try {
    var paths = walkSync(voice_root + req.params.id);
    paths = paths.map(function (name) {
      return voice_url + req.params.id + "/" + name;
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

/** get the voice file
 * <a href="https://github.com/peinan/coeic/wiki/API%E4%BB%95%E6%A7%98_GET:voice">wiki</a>
 */
app.get("/api/voice/:id/:name", function (req, res) {

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