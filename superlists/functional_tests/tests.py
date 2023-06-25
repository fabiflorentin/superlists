from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	# Auxiliary method 
	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)


	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith ouviu falar que agora a aplicação online de lista de tarefas
        # aceita definir prioridades nas tarefas do tipo baixa, média e alta
        # Ela decide verificar a homepage

		self.browser.get(self.live_server_url)

		# Ela percebe que o título da página e o cabeçalho mencionam
		# listas de tarefas com prioridade (priority to-do)

		self.assertIn('Priority To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Priority To-Do', header_text)
		
		#Ela é convidada a inserir um item de tarefa e a prioridade da 
        # mesma imediatamente

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		listPriority = ['alta', 'baixa']
		selectPriority = Select (self.browser.find_element_by_id('id_priority'))
		for i, option in enumerate (selectPriority.options):
			self.assertEqual(option.text, listPriority[i])
		
		
		# Ela digita "Comprar anzol" em uma nova caixa de texto
		# e assinala prioridade alta no campo de seleção de prioridades
		
		inputbox.send_keys('Comprar anzol')
		selectPriority.select_by_value('alta')


		# Quando ela tecla enter, a página é atualizada, e agora
		# a página lista "1 - Comprar anzol - prioridade alta"
		# como um item em uma lista de tarefas
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')

		# Ainda continua havendo uma caixa de texto convidando-a a 
		#  acrescentar outro item. Ela insere "Comprar cola instantâne"
		# e assinala prioridade baixa pois ela ainda tem cola suficiente
		# por algum tempo
		inputbox = self.browser.find_element_by_id('id_new_item')
		selectPriority = Select (self.browser.find_element_by_id('id_priority'))

		inputbox.send_keys("Comprar cola instantânea")  
		selectPriority.select_by_value('baixa')
		inputbox.send_keys(Keys.ENTER)

		# A página é atualizada novamente e agora mostra os dois
		# itens em sua lista
		self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')
		self.wait_for_row_in_list_table('2 - Comprar cola instantânea - prioridade baixa')
		

		# Edith se pergunta se o site lembrará de sua lista. Então
		# ela nota que o site gerou um URL único para ela -- há um 
		# pequeno texto explicativo para isso.

		# Ela acessa essa URL -- sua lista de tarefas continua lá.
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# Satisfeita, ela volta a dormir

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Edith inicia uma nova lista de tarefas
		self.browser.get(self.live_server_url)

		listPriority = ['alta', 'baixa']
		selectPriority = Select (self.browser.find_element_by_id('id_priority'))
		for i, option in enumerate (selectPriority.options):
			self.assertEqual(option.text, listPriority[i])
		

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Comprar anzol')
		selectPriority.select_by_value('alta')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')

		#Ela percebe que sua lista te um URL único
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#Agora um novo usuário, Francis, chega ao site

		## Usamos uma nova versão do nagegador para garantir que nenhuma 
		## informação de Edith está vindo de cookies, etc

		# Fim
