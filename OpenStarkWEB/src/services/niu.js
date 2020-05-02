import request from '@/utils/request';
// api_agenda
export async function ApiGetJob() {
  return request(`/api/agendadata/job`);
}

export async function ApiPostJob(params) {
  return request(`/api/agendadata/job`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiPutJob(params) {
  const { name } = params;
  return request(`/api/agendadata/job/${name}`, {
    method: 'PUT',
    body: params,
  });
}

export async function ApiDeleteJob(params) {
  const { name } = params;
  return request(`/api/agendadata/job/${name}`, {
    method: 'DELETE',
  });
}

export async function ApiPostJobOnce(params) {
  console.log('ApiPostJobOnce:', params);
  return request(`/api/agendadata/job/once`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiPostJobEvery(params) {
  console.log('ApiPostJobEvery:', params);
  return request(`/api/agendadata/job/once`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiPostJobNow(params) {
  console.log('ApiPostJobNow:', params);
  return request(`/api/agendadata/job/now`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiPostJobCancel(params) {
  return request(`/api/agendadata/job/cancel`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiGetJobs(params) {
  if (params) {
    console.log('ApiGetJobs:', params);
  }
  return request(`/api/agendashdata/`);
}

// 已启用
export async function ApiGetUserData(params) {
  const { count } = params;
  if (count) {
    return request(`/api/pydata/plugin/user_data?count=${count}`);
  }
  return request(`/api/pydata/plugin/user_data`);
}

export async function ApiGetHosts(params) {
  const { pid } = params;
  if (pid) {
    return request(`/api/pydata/plugin/get_hosts?pid=${pid}`);
  }
  return request(`/api/pydata/plugin/get_hosts`);
}

export async function ApiGetMobiles(params) {
  const { count } = params;
  if (count) {
    return request(`/api/pydata/plugin/get_many_mobile?count=${count}`);
  }
  return request(`/api/pydata/plugin/get_many_mobile`);
}

export async function ApiPostSwitch(params) {
  const { op, act, host } = params;
  return request(`/api/pydata/plugin/${op}?act=${act}&host=${host}`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiPostRa(params) {
  const { op, act, host } = params;
  return request(`/api/pydata/plugin/${op}?act=${act}&host=${host}`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiPostLoan(params) {
  const { op, act, host } = params;
  return request(`/api/pydata/plugin/${op}?act=${act}&host=${host}`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiPostSingle(params) {
  const { op, act, host } = params;
  return request(`/api/pydata/plugin/${op}?act=${act}&host=${host}`, {
    method: 'POST',
    body: params,
  });
}

export async function ApiGetLoanMock() {
  return request(`/api/pydata/plugin/loan_mock`);
}

export async function ApiGetTasks() {
  return request(`/api/pydata/plugin/tasks`);
}

// 零散数据
export async function ApiGetEnv(params) {
  const { eid, type } = params;

  if (eid) {
    return request(`/api/py/env/detail/list?eid=${eid}&type=${type}`);
  }

  return request(`/api/py/env/server/all`);
}

export async function ApiGetHash(params) {
  const { userId } = params;
  if (userId) {
    return request(`/api/javadata/hashUnencodedChars?userId=${userId}`);
  }

  return request(`/api/javadata/hashUnencodedChars`);
}

export async function ApiGetUserId(params) {
  const { userName, dbHost, dbUser, dbPassword, dbPort } = params;
  return request(`/api/pydata/db/getOneValue`, {
    method: 'POST',
    body: {
      db_info: {
        host: dbHost,
        port: dbPort,
        username: dbUser,
        password: dbPassword,
        db: 'xnaccount',
      },
      sql: `select id from t_user_person where username='${userName}'`,
    },
  });
}

export async function ApiGetRandomUserList(params) {
  const { count, dbHost, dbUser, dbPassword, dbPort } = params;
  return request(`/api/pydata/db/getTable`, {
    method: 'POST',
    body: {
      db_info: {
        host: dbHost,
        port: dbPort,
        username: dbUser,
        password: dbPassword,
        db: 'xnaccount',
      },
      sql: `SELECT t1.id, t1.username FROM t_user_person AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM t_user_person)-(SELECT MIN(id) FROM t_user_person))+(SELECT MIN(id) FROM t_user_person)) AS id) AS t2 WHERE t1.id >= t2.id ORDER BY t1.id LIMIT ${count};`,
    },
  });
}

export async function ApiGetUserName(params) {
  const { userId, dbHost, dbUser, dbPassword, dbPort } = params;
  return request(`/api/pydata/db/getOneValue`, {
    method: 'POST',
    body: {
      db_info: {
        host: dbHost,
        port: dbPort,
        username: dbUser,
        password: dbPassword,
        db: 'xnaccount',
      },
      sql: `select username from t_user_person where id='${userId}'`,
    },
  });
}

export async function ApiGetAccountInfo(params) {
  const { dbHost, dbUser, dbPassword, dbPort, sqlQuery } = params;
  return request(`/api/pydata/db/getTable`, {
    method: 'POST',
    body: {
      db_info: {
        host: dbHost,
        port: dbPort,
        username: dbUser,
        password: dbPassword,
        db: 'xnaccount',
      },
      sql: sqlQuery,
    },
  });
}

export async function ApiGetAccountId(params) {
  const { dbHost, dbUser, dbPassword, dbPort, sqlQuery } = params;
  return request(`/api/pydata/db/getOneValue`, {
    method: 'POST',
    body: {
      db_info: {
        host: dbHost,
        port: dbPort,
        username: dbUser,
        password: dbPassword,
        db: 'xnaccount',
      },
      sql: sqlQuery,
    },
  });
}

export async function ApiUpdateAccount(params) {
  const { dbHost, dbUser, dbPassword, dbPort, sqlUpdate } = params;
  return request(`/api/pydata/db/updateOneValue`, {
    method: 'POST',
    body: {
      db_info: {
        host: dbHost,
        port: dbPort,
        username: dbUser,
        password: dbPassword,
        db: 'xnaccount',
      },
      sql: sqlUpdate,
    },
  });
}

export async function ApiInsertAccount(params) {
  const { dbHost, dbUser, dbPassword, dbPort, sqlInsert } = params;
  return request(`/api/pydata/db/insertOneValue`, {
    method: 'POST',
    body: {
      db_info: {
        host: dbHost,
        port: dbPort,
        username: dbUser,
        password: dbPassword,
        db: 'xnaccount',
      },
      sql: sqlInsert,
    },
  });
}

// 加密登录密码
export async function ApiGetEncryptPassword(params) {
  const { password } = params;
  console.log("ApiGetEncryptPassword:", params);
  if (password) {
    return request(`/api/nodedata/tm/encryptPassword?password=${password}&type=APIDebug`);
  }
  
  return request(`/api/nodedata/tm/encryptPassword?password=t1234567&type=APIDebug`);
}
