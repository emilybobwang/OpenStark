import {
  ApiGetUserData,
  ApiGetHosts,
  ApiGetMobiles,
  ApiGetLoanMock,
  ApiGetEncryptPassword,
  ApiPostRa,
  ApiPostLoan,
  ApiPostSingle,
  ApiGetTasks,
  ApiPostSwitch,
} from '@/services/niu';

export default {
  namespace: 'niu',

  state: {
    UserData: [],
    Hosts: [],
    LoanMock: '',
    Mobiles: [],
    tasks: {},
    messages: '',
    RaMessage: '',
    LoanMessage: '',
    SingleMessage: '',
    SwitchMessage: '',
    password_enc: '',
  },

  effects: {
    *getUserData({ payload }, { call, put }) {
      const response = yield call(ApiGetUserData, payload);
      const { code, message, data } = response;
      if (code === 0) {
        yield put({
          type: 'saveUserData',
          payload: data,
        });
      } else {
        console.log(message);
      }
    },
    *getTasksData({ payload }, { call, put }) {
      const response = yield call(ApiGetTasks, payload);
      const { code, message, result, data } = response;
      if (code === 0) {
        yield put({
          type: 'saveTasks',
          payload: result,
        });
      } else {
        console.log(message, data);
      }
    },
    *getHostsData({ payload }, { call, put }) {
      const response = yield call(ApiGetHosts, payload);
      const { code, message, data } = response;
      if (code === 0) {
        yield put({
          type: 'saveHosts',
          payload: data,
        });
      } else {
        console.log(message);
      }
    },
    *getMobilesData({ payload }, { call, put }) {
      const response = yield call(ApiGetMobiles, payload);
      const { code, message, result, data } = response;
      if (code === 0) {
        yield put({
          type: 'saveMobiles',
          payload: result,
        });
      } else {
        console.log(message, data);
      }
    },
    *getLoanMock({ payload }, { call, put }) {
      const response = yield call(ApiGetLoanMock, payload);
      const { code, message } = response;
      if (code === 0) {
        yield put({
          type: 'saveLoanMock',
          payload: message,
        });
      } else {
        console.log(message);
      }
    },
    *postSwitch({ payload }, { call, put }) {
      yield put({
        type: 'savePostSwitch',
        payload: '',
      });
      const response = yield call(ApiPostSwitch, payload);
      const { code, message, result, data } = response;
      console.log(message, result, data);
      if (code === 0) {
        yield put({
          type: 'savePostSwitch',
          payload: message,
        });
      } else {
        console.log(message, result, data);
      }
    },
    *getEncryptPassword({ payload }, { call, put }){
      const response = yield call(ApiGetEncryptPassword, payload);
      const { code, message, result } = response;
      if (code === 0) {
        yield put({
          type: 'saveEncryptPassword',
          payload: result,
        });
      } else {
        console.log(message);
      }
    },
    *postRa({ payload }, { call, put }) {
      yield put({
        type: 'savePostRa',
        payload: '',
      });
      const response = yield call(ApiPostRa, payload);
      const { code, message, result, data } = response;
      console.log(message, result, data);
      if (code === 0) {
        yield put({
          type: 'savePostRa',
          payload: message,
        });
      } else {
        console.log(message, result, data);
      }
    },
    *postLoan({ payload }, { call, put }) {
      yield put({
        type: 'savePostLoan',
        payload: '',
      });
      const response = yield call(ApiPostLoan, payload);
      const { code, message, result, data } = response;
      console.log(message, result, data);
      if (code === 0) {
        yield put({
          type: 'savePostLoan',
          payload: message,
        });
      } else {
        console.log(message, result, data);
      }
    },
    *postSingle({ payload }, { call, put }) {
      yield put({
        type: 'savePostSingle',
        payload: '',
      });
      const response = yield call(ApiPostSingle, payload);
      const { code, message, result, data } = response;
      console.log(message, result, data);
      if (code === 0) {
        yield put({
          type: 'savePostSingle',
          payload: message,
        });
      } else {
        console.log(message, result, data);
      }
    },
  },

  reducers: {
    saveUserData(state, action) {
      return {
        ...state,
        UserData: action.payload,
      };
    },
    saveHosts(state, action) {
      return {
        ...state,
        Hosts: action.payload,
      };
    },
    saveTasks(state, action) {
      return {
        ...state,
        tasks: action.payload,
      };
    },
    saveMobiles(state, action) {
      return {
        ...state,
        Mobiles: action.payload,
      };
    },
    saveLoanMock(state, action) {
      return {
        ...state,
        LoanMock: action.payload,
      };
    },
    savePostSwitch(state, action) {
      return {
        ...state,
        SwitchMessage: action.payload,
      };
    },
    savePostRa(state, action) {
      return {
        ...state,
        RaMessage: action.payload,
      };
    },
    savePostLoan(state, action) {
      return {
        ...state,
        LoanMessage: action.payload,
      };
    },
    savePostSingle(state, action) {
      return {
        ...state,
        SingleMessage: action.payload,
      };
    },
    saveEncryptPassword(state, action) {
      return {
        ...state,
        password_enc: action.payload,
      };
    },
  },
};
