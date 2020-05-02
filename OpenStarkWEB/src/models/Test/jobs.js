import { message } from 'antd';
import { getJenkins, runJenkins } from '@/services/admin';

export default {
  namespace: 'jobs',

  state: {
    jenkinsJobs: [],
    jenkinsApps: [],
    runResult: undefined,
    reports: {
      data: [],
      size: 0,
      page: 0,
      total: 0,
    },
  },

  effects: {
    *getJenkins({ op, payload, callback }, { call, put }) {
      const response = yield call(getJenkins, op, payload);
      if (op === 'version') {
        if (callback) callback(response && typeof response.data === 'object' ? response.data : {});
      }else{
        yield put({
          type: 'save',
          payload: response && Array.isArray(response.data) ? response.data : [],
          op,
        });
      }
    },
    *runJenkins({ op, payload, callback }, { call, put }) {
      const response = yield call(runJenkins, op, payload);
      yield put({
        type: 'result',
        payload: response,
      });
      if (callback){callback()};
    },
    *fetchReports({ op, payload }, { call, put }) {
      const response = yield call(getJenkins, op, payload);
      yield put({
        type: 'saveReports',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
  },

  reducers: {
    save(state, { payload, op }) {
      if (op === 'apps') {
        return {
          ...state,
          jenkinsApps: payload,
        };
      }
      return {
        ...state,
        jenkinsJobs: payload,
      };
    },
    saveReports(state, { payload }) {
      return {
        ...state,
        reports: payload,
      };
    },
    result(state, { payload }) {
      if (payload && payload.status === 'SUCCESS') {
        message.success(payload.message);
      } else {
        message.error(payload && payload.message);
      }
      return {
        ...state,
        runResult: payload,
      };
    },
  },
};
