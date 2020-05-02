import { routerRedux } from 'dva/router';
import { accountLogin, accountAutoLogin, accountLogout } from '@/services/user';
import { setAuthority } from '@/utils/authority';
import { getPageQuery } from '@/utils/utils';
import { reloadAuthorized } from '@/utils/Authorized';

export default {
  namespace: 'login',

  state: {
    status: undefined,
    message: '',
  },

  effects: {
    *login({ payload }, { call, put }) {
      const response = yield call(accountLogin, payload);
      yield put({
        type: 'changeLoginStatus',
        payload: response,
      });
      // Login successfully
      if (response && response.status === 'SUCCESS') {
        reloadAuthorized();
        const urlParams = new URL(window.location.href);
        const params = getPageQuery();
        let { redirect } = params;
        if (redirect) {
          const redirectUrlParams = new URL(redirect);
          if (redirectUrlParams.origin === urlParams.origin) {
            redirect = redirect.substr(urlParams.origin.length);
            if (redirect.startsWith('/#')) {
              redirect = redirect.substr(2);
            }
          } else {
            window.location.href = redirect;
            return;
          }
        }
        redirect = redirect && redirect.includes('login') ? '/' : redirect;
        yield put(routerRedux.replace(redirect || '/'));
      }
    },
    *autoLogin(_, { call, put }) {
      const response = yield call(accountAutoLogin);
      yield put({
        type: 'changeLoginStatus',
        payload: response,
      });
      // Login successfully
      if (response && response.status === 'SUCCESS') {
        reloadAuthorized();
        const urlParams = new URL(window.location.href);
        const params = getPageQuery();
        let { redirect } = params;
        if (redirect) {
          const redirectUrlParams = new URL(redirect);
          if (redirectUrlParams.origin === urlParams.origin) {
            redirect = redirect.substr(urlParams.origin.length);
            if (redirect.startsWith('/#')) {
              redirect = redirect.substr(2);
            }
          } else {
            window.location.href = redirect;
            return;
          }
        }
        redirect = redirect && redirect.includes('login') ? '/' : redirect;
        yield put(routerRedux.replace(redirect || '/'));
      }
    },
    *logout(_, { put, call }) {
      const response = yield call(accountLogout);
      yield put({
        type: 'changeLoginStatus',
        payload: response,
      });
      if (response && response.status === 'SUCCESS') {
        reloadAuthorized();
        yield put(
          routerRedux.push({
            pathname: '/user/login',
          })
        );
      }
    },
  },

  reducers: {
    changeLoginStatus(state, { payload }) {
      if (payload && payload.status === 'SUCCESS') {
        setAuthority(payload.data.authority);
      } else {
        setAuthority('guest');
      }
      return {
        ...state,
        status: payload && payload.status,
        message: payload && payload.message,
      };
    },
  },
};
