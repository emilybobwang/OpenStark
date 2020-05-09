export default [
  // homepage
  {
    path: '/home',
    component: '../layouts/BlankLayout',
    routes: [{ path: '/home/help', redirect: '/knowledge' }, { component: '404' }],
  },
  // user
  {
    path: '/user',
    component: '../layouts/UserLayout',
    routes: [
      { path: '/user', redirect: '/user/login' },
      { path: 'login', component: './User/Login' },
      { path: 'register', component: './User/Register' },
      { path: 'register-result', component: './User/RegisterResult' },
      { component: '404' },
    ],
  },
  // exception
  {
    path: '/exception',
    component: '../layouts/BlankLayout',
    routes: [
      { path: '/exception', redirect: '/exception/404' },
      {
        path: '403',
        component: './Exception/403',
      },
      {
        path: '404',
        component: './Exception/404',
      },
      {
        path: '500',
        component: './Exception/500',
      },
      { component: '404' },
    ],
  },
  // app
  {
    path: '/',
    component: '../layouts/BasicLayout',
    Routes: ['src/pages/Authorized'],
    routes: [
      { path: '/', redirect: '/dashboard/workplace' },
      {
        name: 'dashboard',
        icon: 'dashboard',
        path: 'dashboard',
        routes: [
          { path: '/dashboard', redirect: '/dashboard/workplace' },
          {
            name: 'workplace',
            icon: 'desktop',
            path: 'workplace',
            component: './Dashboard/Workplace',
          },
          {
            name: 'analysis',
            icon: 'pie-chart',
            path: 'analysis',
            authority: ['admin', 'user'],
            routes: [
              { path: '/dashboard/analysis', redirect: '/dashboard/analysis/tools' },
              {
                name: 'tools',
                path: 'tools',
                component: './Dashboard/Analysis/Tools',
              },
              {
                name: 'auto',
                path: 'auto',
                component: './Dashboard/Analysis/AutoTest',
              },
              {
                name: 'performance',
                path: 'performance',
                component: './Dashboard/Analysis/Performance',
              },
              { component: '404' },
            ],
          },
          {
            name: 'environment',
            icon: 'cloud-o',
            path: 'environment',
            authority: ['admin', 'user'],
            hideChildrenInMenu: true,
            routes: [
              {
                path: '/dashboard/environment',
                component: './Dashboard/Environment/Environment',
              },
              {
                name: 'detail',
                path: 'detail/:dep/:eid',
                component: './Dashboard/Environment/EnvDetail',
              },
              { component: '404' },
            ],
          },
          {
            name: 'projects',
            path: 'projects',
            icon: 'wallet',
            authority: ['admin', 'user'],
            component: './Dashboard/Projects',
          },
          {
            name: 'group',
            icon: 'team',
            path: 'group',
            authority: 'admin',
            component: './Dashboard/Teams/Teams',
          },
          {
            name: 'config',
            icon: 'setting',
            path: 'config',
            authority: 'admin',
            component: './Dashboard/Config/Config',
          },
          { component: '404' },
        ],
      },
      {
        name: 'test',
        icon: 'eye-o',
        path: 'test',
        authority: ['admin', 'user'],
        routes: [
          { path: '/test', redirect: '/test/jobs' },
          {
            name: 'jobs',
            icon: 'schedule',
            path: 'jobs',
            component: './Test/Jobs',
          },
          {
            name: 'reports',
            icon: 'line-chart',
            path: 'reports',
            hideChildrenInMenu: true,
            routes: [
              {
                path: '/test/reports',
                component: './Test/Reports',
              },
              {
                name: 'jacoco',
                path: '/test/reports/jacoco/:jid/:date',
                component: './Test/Details',
              },
              { component: '404' },
            ],
          },
          {
            name: 'testcase',
            icon: 'fork',
            path: 'testcase',
            component: './Test/TestCase',
          },
          { component: '404' },
        ],
      },
      {
        name: 'gui',
        icon: 'laptop',
        path: 'gui',
        authority: ['admin', 'user'],
        routes: [
          { path: '/gui', redirect: '/gui/jobs' },
          {
            name: 'jobs',
            icon: 'schedule',
            path: 'jobs',
            component: './GUITest/Jobs',
          },
          {
            name: 'reports',
            icon: 'line-chart',
            path: 'reports',
            hideChildrenInMenu: true,
            routes: [
              {
                path: '/gui/reports',
                component: './GUITest/Reports/Reports',
              },
              {
                name: 'detail',
                path: 'detail/:jid/:date',
                component: './GUITest/Reports/Detail',
              },
              {
                name: 'jacoco',
                path: '/gui/reports/jacoco/:jid/:date',
                component: './Test/Details',
              },
              { component: '404' },
            ],
          },
          {
            name: 'testcase',
            icon: 'fork',
            path: 'testcase',
            component: './GUITest/TestCase/TestCase',
          },
          { component: '404' },
        ],
      },
      {
        name: 'api',
        icon: 'api',
        path: 'api',
        authority: ['admin', 'user'],
        routes: [
          { path: '/api', redirect: '/api/jobs' },
          {
            name: 'jobs',
            icon: 'schedule',
            path: 'jobs',
            component: './APITest/Jobs',
          },
          {
            name: 'reports',
            icon: 'line-chart',
            path: 'reports',
            hideChildrenInMenu: true,
            routes: [
              {
                path: '/api/reports',
                component: './APITest/Reports/Reports',
              },
              {
                name: 'detail',
                path: 'detail/:jid/:date',
                routes: [
                  {
                    path: '/api/reports/detail/:jid/:date',
                    component: './APITest/Reports/Detail',
                  },
                  {
                    name: 'detail',
                    path: '/api/reports/detail/case/:jid/:date/:cid',
                    component: './APITest/Reports/CaseDetail',
                  },
                  { component: '404' },
                ],
              },
              {
                name: 'jacoco',
                path: '/api/reports/jacoco/:jid/:date',
                component: './Test/Details',
              },
              { component: '404' },
            ],
          },
          {
            name: 'testcase',
            icon: 'fork',
            path: 'testcase',
            hideChildrenInMenu: true,
            routes: [
              {
                path: '/api/testcase',
                component: './APITest/TestCase/TestCase',
              },
              {
                name: 'detail',
                path: 'detail/:pid/:cid',
                component: './APITest/TestCase/TestCaseDetail',
              },
              { component: '404' },
            ],
          },
          {
            name: 'debug',
            icon: 'exception',
            hideInMenu: true,
            path: 'debug',
          },
          {
            name: 'config',
            icon: 'setting',
            path: 'config',
            hideInMenu: true,
            routes: [
              { path: '/api/config', redirect: '/config/interface' },
              {
                name: 'interface',
                path: 'interface',
              },
              {
                name: 'crypt',
                path: 'crypt',
              },
              { component: '404' },
            ],
          },
          { component: '404' },
        ],
      },
      {
        name: 'tool',
        path: 'tools',
        icon: 'tool',
        authority: ['admin', 'user'],
        routes: [
          { path: '/tools', redirect: '/tools/manage' },
          {
            name: 'deploy',
            icon: 'deployment-unit',
            path: 'deploy',
            routes: [
              { path: '/tools/deploy', redirect: '/tools/deploy/syncDB' },
              {
                name: 'syncDB',
                path: 'syncDB',
                component: './Tools/Deploy/SyncDB',
              },
              {
                name: 'reDB',
                path: 'reDB',
                component: './Tools/Deploy/ReDB',
              },
              { component: '404' },
            ],
          },
          {
            name: 'version',
            icon: 'file-sync',
            path: 'version',
            routes: [
              { path: '/tools/version', redirect: '/tools/version/diffDB' },
              {
                name: 'diffDB',
                path: 'diffDB',
                component: './Tools/Deploy/DiffDB',
              },
              {
                name: 'diffAPP',
                path: 'diffAPP',
                component: './Tools/Deploy/DiffAPP',
              },
              { component: '404' },
            ],
          },
          {
            name: 'scripts',
            icon: 'code-o',
            path: 'scripts',
            routes: [
              { path: '/tools/scripts', redirect: '/tools/scripts/shell' },
              {
                name: 'shell',
                path: 'shell',
                component: './Tools/Shell/Shell',
                routes: [
                  { path: '/tools/scripts/shell', redirect: '/tools/scripts/shell/0' },
                  {
                    path: ':id',
                    component: './Tools/Shell/ShellForm',
                  },
                  { component: '404' },
                ],
              },
              {
                name: 'sql',
                path: 'sql',
                component: './Tools/SQL/SQL',
                routes: [
                  { path: '/tools/scripts/sql', redirect: '/tools/scripts/sql/0' },
                  {
                    path: ':id',
                    component: './Tools/SQL/SQLForm',
                  },
                  { component: '404' },
                ],
              },
              { component: '404' },
            ],
          },
          {
            name: 'encrypt',
            icon: 'lock',
            path: 'encrypt',
            hideInMenu: true,
          },
          {
            name: 'decrypt',
            icon: 'unlock',
            path: 'decrypt',
            hideInMenu: true,
          },
          {
            name: 'others',
            icon: 'appstore',
            path: 'others',
            component: './Tools/Others/Others',
            routes: [
              { path: '/tools/others', redirect: '/tools/others/0' },
              {
                path: ':id',
                component: './Tools/Deploy/IFrame',
              },
              { component: '404' },
            ],
          },
          {
            name: 'manage',
            path: 'manage',
            icon: 'setting',
            component: './Tools/Manger/Tools',
          },
          { component: '404' },
        ],
      },
      {
        name: 'account',
        path: 'account',
        hideInMenu: true,
        routes: [
          { path: '/account', redirect: '/account/settings' },
          {
            name: 'settings',
            path: 'settings',
            component: './Account/Settings/Info',
            routes: [
              { path: '/account/settings', redirect: '/account/settings/base' },
              {
                path: 'base',
                component: './Account/Settings/BaseView',
              },
              {
                path: 'passwd',
                component: './Account/Settings/Passwd',
              },
              {
                path: 'nav',
                component: './Profile/Setting/Setting',
              },
              { component: '404' },
            ],
          },
          { component: '404' },
        ],
      },
      {
        name: 'knowledge',
        path: 'knowledge',
        authority: ['admin', 'user'],
        icon: 'zhihu',
        routes: [
          { path: '/knowledge', redirect: '/knowledge/books' },
          {
            name: 'books',
            path: 'books',
            icon: 'book',
            hideChildrenInMenu: true,
            routes: [
              {
                path: '/knowledge/books',
                component: './Knowledge/Books/Books',
              },
              {
                name: 'edit',
                path: 'edit/:key',
                component: './Knowledge/Books/Editor',
              },
              {
                name: 'blog',
                path: 'blog/:cid',
                component: './Knowledge/Books/BlogList',
                routes: [
                  { path: '/knowledge/books/blog', redirect: '/knowledge/books' },
                  { path: '/knowledge/books/blog/:cid', redirect: '/knowledge/books/blog/:cid/0' },
                  {
                    path: ':bid',
                    component: './Knowledge/Books/Blog',
                  },
                  { component: '404' },
                ],
              },
              { component: '404' },
            ],
          },
          {
            name: 'online',
            path: 'online',
            icon: 'alert',
            hideChildrenInMenu: true,
            routes: [
              {
                path: '/knowledge/online',
                component: './Knowledge/Online/Online',
              },
              {
                name: 'edit',
                path: 'edit/:key',
                component: './Knowledge/Online/OnlineEdit',
              },
              { component: '404' },
            ],
          },
          { component: '404' },
        ],
      },
      { component: '404' },
    ],
  },
];
