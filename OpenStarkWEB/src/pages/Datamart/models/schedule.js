import {
  ApiDeleteJob,
  ApiGetJob,
  ApiGetJobs,
  ApiPostJob,
  ApiPostJobCancel,
  ApiPostJobEvery,
  ApiPostJobNow,
  ApiPostJobOnce,
  ApiPutJob,
} from '../../../services/niu';

export default {
  namespace: 'schedule',

  state: {
    jobs: null,
    runMode: 0, // 0: 周期调度，1：单次调度， 2： 立即调度
    currentJobs: {
      name: 'default',
      interval: '',
      data: {
        headers: {},
        params: {},
        query: {},
        body: '',
      },
    },
    result: '',
    op: 0,
    current: {
      name: 'default',
      url: 'http://172.20.20.160:8097/api/echo',
    },
    list: [],
  },

  effects: {
    *getJobs(_, { call, put }) {
      const response = yield call(ApiGetJobs);
      yield put({
        type: 'save',
        payload: { jobs: response },
      });
    },
    *getJob(_, { call, put }) {
      const response = yield call(ApiGetJob);
      yield put({
        type: 'save',
        payload: { list: response },
      });
    },
    *newJob(_, { call, put, select }) {
      const obj = yield select(state => state.schedule.current);
      const response = yield call(ApiPostJob, { ...obj });
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJob' });
    },
    *newJobs(_, { call, put, select }) {
      const runMode = yield select(state => state.schedule.runMode);
      if (runMode === 0) {
        yield put({ type: 'runEvery' });
      } else if (runMode === 1) {
        yield put({ type: 'runOnce' });
      } else if (runMode === 2) {
        yield put({ type: 'runNow' });
      } else {
        console.log('newJobs: 未处理的runMode/', runMode);
      }
    },
    *runNow(_, { call, put, select }) {
      const { interval, ...restField } = yield select(state => state.schedule.currentJobs);
      const response = yield call(ApiPostJobNow, { ...restField });
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJobs' });
    },
    *runOnce(_, { call, put, select }) {
      const obj = yield select(state => state.schedule.currentJobs);
      const response = yield call(ApiPostJobOnce, { ...obj });
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJobs' });
    },
    *runEvery(_, { call, put, select }) {
      const obj = yield select(state => state.schedule.currentJobs);
      const response = yield call(ApiPostJobEvery, { ...obj });
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJobs' });
    },
    *runCancel(_, { call, put, select }) {
      const obj = yield select(state => state.schedule.currentJobs);
      const response = yield call(ApiPostJobCancel, { ...obj });
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJobs' });
    },
    *updateJob(_, { call, put, select }) {
      const obj = yield select(state => state.schedule.current);
      const response = yield call(ApiPutJob, { ...obj });
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJob' });
    },
    *copyJob({ payload }, { put, select }) {
      const { name, op = 0 } = payload;
      const list = yield select(state => state.schedule.list);
      for (const job of list) {
        const { _id, name: srcName, url, method, callback } = job;
        if (name === srcName) {
          // 规避深层复制问题
          const current = {
            name: op === 0 ? `${name}_copy` : name,
            url,
            method: method || 'POST',
          };
          if (callback) {
            current.callback = {
              url: callback.url || '',
              method: callback.method || 'POST',
              headers: {
                ...callback.headers,
              },
            };
          }
          yield put({
            type: 'save',
            payload: { current, op },
          });
          break;
        }
      }
    },
    *deleteJob({ payload }, { call, put }) {
      const response = yield call(ApiDeleteJob, payload);
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJob' });
    },
    *runJobOnce({ payload }, { call, put }) {
      const response = yield call(ApiPostJobOnce, payload);
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJob' });
    },
    *runJobEvery({ payload }, { call, put }) {
      const response = yield call(ApiPostJobEvery, payload);
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJob' });
    },
    *runJobNow({ payload }, { call, put }) {
      const response = yield call(ApiPostJobNow, payload);
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJob' });
    },
    *cancelJob({ payload }, { call, put }) {
      const response = yield call(ApiPostJobCancel, payload);
      yield put({
        type: 'save',
        payload: { result: response },
      });

      yield put({ type: 'getJob' });
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
  },
};
