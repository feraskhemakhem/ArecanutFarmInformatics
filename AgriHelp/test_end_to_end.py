# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:08:44 2022

@author: siri namburi
"""

import unittest
from datetime import datetime,timedelta
from random import randint


import app as AFI_UI
from rds_db import insert_new_user,get_user,get_user_list,add_plot,conn,get_plot

class TestEndtoEnd(unittest.TestCase):

    def setUp(self):
       AFI_UI.app.testing = True
       self.app = AFI_UI.app.test_client(self)
       self._register_details()

    def _register_details(self):
        try:
            response = self.app.post('/login',
                data = dict(Username='test',password='test')
                )
            assert response.status_code == 200

        except:
            response = self.app.post('/signup',
            data = dict(Username='test',email='test@gmail.com',password = 'test',password2='test'))
        
            assert response.status_code == 200


    def testlogin(self):
        response = self.app.post('/login',
            data = dict(Username="test", password="test"))
        assert response.status_code==200
       
    def test_home_page(self):
        response = self.app.get("/")
        assert response.status_code == 200        
    
    def test_tank_input_form(self):

        response = self.app.post('/tankinput',
            data= dict(tank_name='tstcir'+str(randint(0,1000000)),
                TANK='circle',
                diameter=1,cheight=1))

        assert response.status_code == 200

        response = self.app.post('/tankinput',
            data= dict(tank_name='tstrec'+str(randint(0,1000000)),TANK='rectangle',
                length=1,depth=1,width=1))
        assert response.status_code == 200

        response = self.app.post('/tankinput',
            data= dict(tank_name='tstnorm'+str(randint(0,1000000)),
                top1=1,top2=1,base1=1,base2=1,height=1))
        assert response.status_code == 200

    def test_rainfall_input(self):
        response = self.app.post('/rainfallinput',
            data = dict(date=datetime.today().date(),rainfall = 1) 
            )
        assert response.status_code==200

    def test_irrigation_schedule(self):
        response = self.app.post('/irrigationschedule',
            data = dict(start_date=[datetime.today().date()]*3,
                start_time = [datetime.now()]*3,
                end_time =[datetime.now()+timedelta(minutes=1)]*3 ,
                frequency=[1]*3,

                )

            )
        assert response.status_code==200


class TestDB(unittest.TestCase):
    def setUp(self):
        self.user_details= dict(username='testdb',email='testdb@gmail.com',password = 'test_db')
        self._delete_user()

        insert_new_user(self.user_details['username'], self.user_details['email'], self.user_details['password'], self.user_details['password'])

        self.plot_details = dict( _plot_name='testdb_plot', _plot_size=1)
        add_plot([self.user_details['username']], [self.plot_details['_plot_name']], [self.plot_details['_plot_size']])
        

    def _delete_user(self):
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM Users WHERE username = %s", (self.user_details['username']))
        usr_det = cur.fetchone()

        if usr_det:
            cur.execute("DELETE FROM Plots WHERE username = %s;", (self.user_details['username']))
            cur.execute("DELETE FROM Users WHERE username = %s;", (self.user_details['username']))
            conn.commit()



        

    def test_user(self):
        all_users = get_user_list()
        assert all_users
        _user_id = get_user(self.user_details['username'], self.user_details['password'])
        for each in all_users:
            if each[0]==_user_id:
                assert each[1]==self.user_details['username']
                assert each[2]==self.user_details['email']
                assert each[3]==self.user_details['password']
                break
        
        
        
    def test_plot_inputs(self):
        _plot_details  = get_plot(self.user_details['username'])[0]
        assert _plot_details[0] == self.plot_details['_plot_name']
        assert int(_plot_details[1]) == self.plot_details['_plot_size']



if __name__ == '__main__':
    unittest.main()