import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const routes = [
  {
    path: '*',
    redirect: '/vote'
  },
  {
    name: 'index',
    component: () => import('./view/index'),
    meta: {
      title: '首页'
    }
  },
  {
    name: 'admin',
    component: () => import('./view/admin'),
    meta: {
      title: '管理员界面'
    }
  },
  {
    name: 'vote',
    component: () => import('./view/vote'),
    meta: {
      title: '风采展示',
      keepAlive: true
    },
    props: true,
  },
  {
    name: 'pdf',
    component: () => import('./view/pdf'),
    meta: {
      title: '',
    },
    props: true
  }
];

// add route path
routes.forEach(route => {
  route.path = route.path || '/' + (route.name || '');
});

const router = new Router({ routes });

router.beforeEach((to, from, next) => {
  const title = to.meta && to.meta.title;
  if (title) {
    document.title = title;
  }
  next();
});

export {
  router
};
