import {
  ApiGetEnv,
  ApiGetHash,
  ApiGetUserId,
  ApiGetAccountId,
  ApiInsertAccount,
  ApiUpdateAccount,
  ApiGetAccountInfo,
  ApiGetRandomUserList,
  ApiGetUserName,
} from '@/services/niu';

export default {
  namespace: 'assistant',

  state: {
    EnvData: [],
    CurrentEnvData: [],
    AccountTableOutput: [],
    userIdHashValue: '0',
    userId: 0,
    userName: '',
    accountId: '',
    accountInfo: '',
    insertAccount: '',
    updateAccount: '',
    sqlQuery: '',
    sqlQueryInfo: '',
    sqlInsert: '',
    sqlUpdate: '',
  },

  effects: {
    *getRandomUserList({ payload }, { call, put }) {
      const response = yield call(ApiGetRandomUserList, payload);
      const { code, message, result = [], data } = response;
      if (code === 0) {
        yield put({
          type: 'save',
          payload: { userRandomList: result },
        });
      } else {
        console.log(message, data);
      }
    },
    *getEnvData({ payload }, { call, put }) {
      const response = yield call(ApiGetEnv, payload);
      const { status, message, data } = response;

      if (status === 'SUCCESS') {
        const { eid } = payload;
        if (eid === undefined) {
          yield put({
            type: 'saveEnvData',
            payload: data.data,
          });
        } else {
          yield put({
            type: 'saveCurrentEnvData',
            payload: data.data,
          });
        }
      } else {
        console.log(message);
      }
    },
    *getHashData({ payload }, { call, put }) {
      const response = yield call(ApiGetHash, payload);
      const { code, message, result } = response;
      if (code === 0) {
        yield put({
          type: 'saveHashData',
          payload: result,
        });
      } else {
        console.log(message);
      }
    },
    *getUserId({ payload }, { call, put }) {
      const response = yield call(ApiGetUserId, payload);
      const { code, message, result } = response;
      if (code === 0) {
        yield put({
          type: 'saveUserId',
          payload: result,
        });
      } else {
        console.log(message);
      }
    },
    *getAccountInfo({ payload }, { call, put }) {
      const { sqlQuery } = payload;
      yield put({
        type: 'saveQueryAccountInfo',
        payload: sqlQuery,
      });

      const response = yield call(ApiGetAccountInfo, payload);
      const { code, message, result } = response;
      if (code === 0) {
        yield put({
          type: 'saveAccountInfo',
          payload: result,
        });
      } else {
        console.log(message);
      }
    },
    *getAccountId({ payload }, { call, put }) {
      const { sqlQuery } = payload;
      yield put({
        type: 'saveQueryAccountSql',
        payload: sqlQuery,
      });

      const response = yield call(ApiGetAccountId, payload);
      const { code, message, result } = response;
      if (code === 0) {
        yield put({
          type: 'saveAccountId',
          payload: result,
        });
      } else {
        console.log(message);
      }
    },
    *insertAccount({ payload }, { call, put }) {
      const response = yield call(ApiInsertAccount, payload);
      const { sqlInsert } = payload;
      yield put({
        type: 'saveInsertAccountSql',
        payload: sqlInsert,
      });

      const { code, message, result } = response;
      if (code === 0) {
        yield put({
          type: 'saveInsertAccount',
          payload: result,
        });
      } else {
        console.log(message);
      }
    },
    *updateAccount({ payload }, { call, put }) {
      const { sqlUpdate } = payload;
      yield put({
        type: 'saveUpdateAccountSql',
        payload: sqlUpdate,
      });
      const response = yield call(ApiUpdateAccount, payload);
      const { code, message, result } = response;
      if (code === 0) {
        yield put({
          type: 'saveUpdateAccount',
          payload: result,
        });
      } else {
        console.log(message);
      }
    },
    *updateUserName({ payload }, { put }) {
      const { userName } = payload;
      yield put({
        type: 'save',
        payload: { userName },
      });
      yield put({
        type: 'getUserId',
        payload,
      });
    },
    *updateUserId({ payload }, { put, call }) {
      const { userId } = payload;
      yield put({
        type: 'save',
        payload: { userId },
      });
      yield put({
        type: 'getHashData',
        payload: { userId },
      });

      try {
        const response = yield call(ApiGetUserName, payload);
        if (response) {
          const { code, message, result = {}, data } = response;
          if (code === 0) {
            yield put({
              type: 'save',
              payload: { userName: result },
            });
          } else {
            console.log('updateUserId:', message, data);
          }
        }
      } catch {
        yield put({
          type: 'save',
          payload: { userName: '' },
        });
      }
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
    saveEnvData(state, action) {
      return {
        ...state,
        EnvData: action.payload,
      };
    },
    saveInsertAccount(state, action) {
      return {
        ...state,
        insertAccount: action.payload,
      };
    },
    saveInsertAccountSql(state, action) {
      return {
        ...state,
        sqlInsert: action.payload,
      };
    },
    saveQueryAccountSql(state, action) {
      return {
        ...state,
        sqlQuery: action.payload,
      };
    },
    saveQueryAccountInfo(state, action) {
      return {
        ...state,
        sqlQueryInfo: action.payload,
      };
    },
    saveUpdateAccount(state, action) {
      return {
        ...state,
        updateAccount: action.payload,
      };
    },
    saveUpdateAccountSql(state, action) {
      return {
        ...state,
        sqlUpdate: action.payload,
      };
    },
    saveUserId(state, action) {
      return {
        ...state,
        userId: action.payload,
      };
    },
    saveAccountInfo(state, action) {
      return {
        ...state,
        accountInfo: action.payload,
      };
    },
    saveAccountId(state, action) {
      return {
        ...state,
        accountId: action.payload,
      };
    },
    saveHashData(state, action) {
      return {
        ...state,
        userIdHashValue: action.payload,
      };
    },
    saveCurrentEnvData(state, action) {
      return {
        ...state,
        CurrentEnvData: action.payload,
      };
    },
  },
};
