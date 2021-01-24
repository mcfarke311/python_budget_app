class Category:
  def __init__(self, category_name):
    self.categoryName = category_name
    self.ledger = []
    self.spent_within_category = 0

  def __str__(self):
    lines = []
    lines.append(self.categoryName.center(30, '*'))
    for item in self.ledger:
      lines.append("{0:23.23s}{1:>7.2f}".format(item['description'], item['amount']))
    lines.append("Total: {0:.2f}".format(self.get_balance()))
    return '\n'.join(lines)

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
    balance = self.get_balance()
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      self.spent_within_category += amount
      return True
    return False

  def get_balance(self):
    balance = 0
    for transaction in self.ledger:
      balance += transaction['amount']
    return balance

  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {category.categoryName}")
      category.deposit(amount, f"Transfer from {self.categoryName}")
      return True
    return False

  def check_funds(self, amount):
    balance = self.get_balance()
    if amount > balance:
      return False
    return True


def create_spend_chart(categories):
  final_string_to_join = []
  final_string_to_join.append("Percentage spent by category")

  chart_width = len(categories) * 3 + 1
  # get the total spent so that we can form the percentage by category
  total_spent = 0
  for category in categories:
    total_spent += category.spent_within_category

  percentages = []
  labels = []
  for category in categories:
    # since we are in categories, lets go ahead and get the names of the categories for making the labels
    labels.append(category.categoryName)
    # get percentage by category and round down to nearest 10 percent
    percentage = int((category.spent_within_category / total_spent) * 100)
    percentage = (percentage // 10) * 10
    percentages.append(percentage)

  # NOTE: The indexes of the percentages list and the labels list should match up

  # populate chart with percentage data
  for percentValue in range(100, -10, -10):
    line = "{0:>3d}|".format(percentValue)
    for percentage in percentages:
      # if there is a bar here, print it
      if percentage >= percentValue:
        line += " o "
      else: # else we put 3 spaces
        line += "   "
    line += " " # final space on the end
    final_string_to_join.append(line)

  # put the bar across the bottom of the chart
  chart_footer = "-" * chart_width
  final_string_to_join.append(chart_footer.rjust(chart_width + 4))

  maxLabelLength = max([len(label) for label in labels])
  for i in range(maxLabelLength):
    line = " " * 4
    for label in labels:
      try:
        line += " %c " % label[i]
      except IndexError:
        line += "   "
    line += " "
    final_string_to_join.append(line)

  return('\n'.join(final_string_to_join))