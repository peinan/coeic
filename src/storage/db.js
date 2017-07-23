'use strict';

process.on('unhandledRejection', console.dir);

const mysql = require('mysql');
const pool = mysql.createPool({
  connectionLimit: 10,
  host: '35.188.103.34',
  user: 'root',
  password: 'hackday14_coeic',
  database: 'coeic_db'
});

/**
 * create table if not exists
 */
pool.getConnection(function (err, connection) {
  // use the connection
  connection.query('CREATE TABLE IF NOT EXISTS `uploaded_imgs` (' +
    '  `id`         INTEGER PRIMARY KEY AUTO_INCREMENT,' +
    '  `filename`   VARCHAR(255),' +
    '  `status`     VARCHAR(255),' +
    '  `message`    VARCHAR(255),' +
    '  `created_at` DATETIME NOT NULL,' +
    '  `updated_at` DATETIME NOT NULL' +
    ');', function (error) {
    // And done with the connection.
    connection.release();
    // Handle error after the release.
    if (error) throw error;
  })
});

const STATUS_TODO = 'TODO';
const STATUS_DOING = 'DOING';
const STATUS_DONE = 'DONE';
const STATUS_FAILED = 'TODO';

module.exports = {

  STATUS_TODO: STATUS_TODO,
  STATUS_DOING: STATUS_DOING,
  STATUS_DONE: STATUS_DONE,
  STATUS_FAILED: STATUS_FAILED,

  /**
   * select all images
   */
  selectMulti: function (max_num) {
    return new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        connection.query({
          sql: 'SELECT * FROM `uploaded_imgs` ORDER BY id DESC LIMIT ?;',
          timeout: 60000,
          values: [max_num]
        }, function (error, results) {
          connection.release();
          if (error) return reject(error);
          resolve(results);
        })
      });
    });
  },

  /**
   * select image by id
   */
  select: function (id) {
    return new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        connection.query({
          sql: 'SELECT * FROM `uploaded_imgs` WHERE id = ?;',
          timeout: 60000,
          values: [id]
        }, function (error, results) {
          connection.release();
          if (error) return reject(error);
          resolve(results);
        })
      });
    });
  },

  /**
   * select specified status images
   */
  selectStatus: function (status) {
    return new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        connection.query({
          sql: 'SELECT * FROM `uploaded_imgs` WHERE status = ?;',
          timeout: 60000,
          values: [status]
        }, function (error, results) {
          connection.release();
          if (error) return reject(error);
          resolve(results);
        })
      });
    });
  },

  /**
   * select an idling image whose id is smallest
   */
  selectNext: function () {
    // 処理中の画像があるかチェック
    const doing = new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        connection.query({
          sql: 'SELECT * FROM `uploaded_imgs` WHERE status = ?;',
          timeout: 60000,
          values: [STATUS_DOING]
        }, function (error, results) {
          connection.release();
          if (error) return reject(error);
          resolve(results);
        })
      });
    }).then(function (result) {
      return result;
    }).catch(function (err) {
      throw err;
    });
    // 処理中の画像があれば空を返す
    if (doing.length > 0) {
      return [];
    }

    // 処理待ちの画像で最もidが若いものを探して返す
    return new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        connection.query({
          sql: 'SELECT * FROM `uploaded_imgs` WHERE status = ? ORDER BY id LIMIT 1;',
          timeout: 60000,
          values: [STATUS_TODO]
        }, function (error, results) {
          connection.release();
          if (error) return reject(error);
          resolve(results);
        })
      });
    });
  },

  /**
   * insert a row into database and get
   */
  insert: function (filename, status, message) {
    return new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        connection.query({
          sql: 'INSERT INTO `uploaded_imgs` (filename, status, message, created_at, updated_at) VALUES (?, ?, ?, NOW(), NOW())',
          timeout: 60000,
          values: [filename, status, message]
        }, function (error, results) {
          connection.release();
          if (error) return reject(error);
          resolve(results);
        })
      });
    });
  },

  /**
   * update status, message and updated time
   */
  update: function (id, status, message) {
    return new Promise(function (resolve, reject) {
      pool.getConnection(function (err, connection) {
        connection.query({
          sql: 'UPDATE `uploaded_imgs` SET status = ?,  message = ?, updated_at = NOW() WHERE id = ?',
          timeout: 60000,
          values: [status, message, id]
        }, function (error, results) {
          connection.release();
          if (error) return reject(error);
          resolve(results);
        })
      });
    });
  }
}