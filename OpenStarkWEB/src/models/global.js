import { message } from 'antd';
import { queryNotices, getCommonInfo, clearNotices, sendMail } from '@/services/global';

export default {
  namespace: 'global',

  state: {
    collapsed: false,
    notices: [],
    commonInfo: {},
    respMsg: undefined,
    loadedAllNotices: false,
  },

  effects: {
    *fetchNotices(_, { call, put, select }) {
      const response = yield call(queryNotices);
      const data = response && Array.isArray(response.data) ? response.data : [];
      const loadedAllNotices = data && data.length && data[data.length - 1] === null;
      yield put({
        type: 'setLoadedStatus',
        payload: loadedAllNotices,
      });
      yield put({
        type: 'saveNotices',
        payload: data.filter(item => item),
      });
      const unreadCount = yield select(
        state => state.global.notices.filter(item => !item.read).length
      );
      yield put({
        type: 'user/changeNotifyCount',
        payload: {
          totalCount: data.length,
          unreadCount,
        },
      });
    },
    *fetchMoreNotices({ payload }, { call, put, select }) {
      const response = yield call(queryNotices, payload);
      const data = response && Array.isArray(response.data) ? response.data : [];
      const loadedAllNotices = data && data.length && data[data.length - 1] === null;
      yield put({
        type: 'setLoadedStatus',
        payload: loadedAllNotices,
      });
      yield put({
        type: 'pushNotices',
        payload: data.filter(item => item),
      });
      const unreadCount = yield select(
        state => state.global.notices.filter(item => !item.read).length
      );
      yield put({
        type: 'user/changeNotifyCount',
        payload: {
          totalCount: data.length,
          unreadCount,
        },
      });
    },
    *clearNotices({ payload }, { call, put, select }) {
      const response = yield call(clearNotices, { type: payload });
      yield put({
        type: 'saveClearedNotices',
        payload: {
          type: payload,
          ...response,
        },
      });
      const count = yield select(state => state.global.notices.length);
      const unreadCount = yield select(
        state => state.global.notices.filter(item => !item.read).length
      );
      yield put({
        type: 'user/changeNotifyCount',
        payload: {
          totalCount: count,
          unreadCount,
        },
      });
    },
    *changeNoticeReadState({ payload }, { call, put, select }) {
      const response = yield call(clearNotices, { type: 'read', mid: payload });
      message.success(response.message);
      const notices = yield select(state =>
        state.global.notices.map(item => {
          const notice = { ...item };
          if (notice.id === payload) {
            notice.read = true;
          }
          return notice;
        })
      );
      yield put({
        type: 'saveNotices',
        payload: notices,
      });
      yield put({
        type: 'user/changeNotifyCount',
        payload: {
          totalCount: notices.length,
          unreadCount: notices.filter(item => !item.read).length,
        },
      });
    },
    *fetchCommonInfo(_, { call, put }) {
      const response = yield call(getCommonInfo);
      yield put({
        type: 'commonInfo',
        payload: response && typeof response.data === 'object' ? response.data : {},
      });
    },
    *sendMail({ op, payload }, { call, put }) {
      const response = yield call(sendMail, op, payload);
      yield put({
        type: 'save',
        payload: response,
      });
    },
  },

  reducers: {
    save(state, { payload }) {
      if (payload && payload.status === 'SUCCESS') {
        message.success(payload.message);
      } else {
        message.error(payload && payload.message);
      }
      return {
        ...state,
        respMsg: payload,
      };
    },
    changeLayoutCollapsed(state, { payload }) {
      return {
        ...state,
        collapsed: payload,
      };
    },
    saveNotices(state, { payload }) {
      return {
        ...state,
        notices: payload,
      };
    },
    saveClearedNotices(state, { payload }) {
      if (payload && payload.status === 'FAIL') {
        message.error(payload && `清空${payload.type}失败`);
      }
      return {
        ...state,
        notices: state.notices.filter(item => item.type !== payload.type),
      };
    },
    pushNotices(state, { payload }) {
      return {
        ...state,
        notices: [...state.notices, ...payload],
      };
    },
    setLoadedStatus(state, { payload }) {
      return {
        ...state,
        loadedAllNotices: payload,
      };
    },
    commonInfo(state, { payload }) {
      return {
        ...state,
        commonInfo: payload,
      };
    },
  },

  subscriptions: {
    setup({ history }) {
      // Subscribe history(url) change, trigger `load` action if pathname is `/`
      return history.listen(({ pathname, search }) => {
        if (typeof window.ga !== 'undefined') {
          window.ga('send', 'pageview', pathname + search);
        }
      });
    },
  },
};
