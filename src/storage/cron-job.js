'use strict';

if (process.argv.length < 5) {
  throw Error("Usage: " + process.argv.join(" ") + " <storage_root_path> <python_command> <script_name>")
}

const db = require('./db');

// 実際に保存されるストレージのルート
const storage_root = process.argv[2].endsWith("/") ? process.argv[2] : process.argv[2] + "/";

// python command
const python = process.argv[3];

// python script
const script = process.argv[4];

const cron = require('node-cron');
const cmd  = require('node-cmd');

/**
 * 処理をキックするcron job
 */
cron.schedule('*/1 * * * * *', function(){

  // DBに接続して次に処理すべき画像があるかチェックし，あれば処理を起動
  db.selectNext().then(function (results) {
    if (results.length === 0) {
      console.log("nothing to do");
      return;
    }

    const to_be_processed = results[0];

    // DBを更新する
    db.update(to_be_processed.id, db.STATUS_DOING, to_be_processed.message).then(function () {
      console.log("update info of " + to_be_processed.filename);
      console.log("DB update succeeded: " + db.STATUS_DOING);
    }).catch(function (err) {
      console.log("DB update failed. reason: " + err.toString());
    });

    // パスを生成
    const img_path = storage_root + to_be_processed.id + '/' + to_be_processed.filename;

    // run python script
    cmd.get(python + ' ' + script + ' ' + img_path,
      function (err, stdout) {

        if (!err) {
          console.log("data from python script: " + stdout);

          try {
            const data = JSON.parse(stdout);
            const path = require('path');

            // 成功か失敗か判定
            const status = data.job_result.status;
            const message = stdout;
            let progress = db.STATUS_DONE;
            if (status !== 'SUCCEEDED') {
              progress = db.STATUS_FAILED;
            }

            // DBの情報を更新する
            console.log("update info of " + to_be_processed.filename);
            db.updateByName(to_be_processed.filename, progress, message).then(function () {
              console.log("DB update succeeded: " + progress);
            }).catch(function (err) {
              console.log("DB update failed: " + err);
            });
          } catch (e) {
            console.log("data parse failed: " + e);
            console.log("update info of " + to_be_processed.filename);
            db.updateByName(to_be_processed.filename, db.STATUS_FAILED, e.stack).then(function () {
              console.log("DB update succeeded: " + db.STATUS_FAILED);
            }).catch(function (err) {
              console.log("DB update failed: " + err);
            });
          }
        } else {
          console.log("python script cmd error: " + err);
          console.log("update info of " + to_be_processed.filename);
          db.updateByName(to_be_processed.filename, db.STATUS_FAILED, err.toString()).then(function () {
            console.log("DB update succeeded: " + db.STATUS_FAILED);
          }).catch(function (err) {
            console.log("DB update failed: " + err);
          });
        }
      });
  }).catch(function (err) {
    console.log("DB check failed: " + err);
  })
});