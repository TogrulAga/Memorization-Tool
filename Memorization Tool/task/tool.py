from sqlalchemy import create_engine
from table import Base, FlashCard
from sqlalchemy.orm import sessionmaker


class MemorizationTool:
    def __init__(self):
        self.engine = None
        self.session = None
        self.setup_orm()
        self.start_session()
        self.show_menu()

    def setup_orm(self):
        self.engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)

    def start_session(self):
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def show_menu(self):
        while True:
            print("1. Add flashcards")
            print("2. Practice flashcards")
            print("3. Exit")
            try:
                answer = input()
                answer = int(answer)
            except ValueError:
                print(f"{answer} is not an option")
                continue
            print()
            if answer == 1:
                self.add_flashcard()
            elif answer == 2:
                self.practice_flashcards()
            elif answer == 3:
                print("Bye!")
                return
            else:
                print(f"{answer} is not an option")

    def add_flashcard(self):
        while True:
            print("1. Add a new flashcard")
            print("2. Exit")
            try:
                answer = input()
                answer = int(answer)
            except ValueError:
                print(f"{answer} is not an option")
                continue
            print()
            if answer == 1:
                while True:
                    question = input("Question:\n")
                    if len(question) > 10:
                        break
                while True:
                    answer = input("Answer:\n")
                    if len(answer) > 1:
                        break
                self.save_to_db(question, answer)
                print()
            elif answer == 2:
                return
            else:
                print(f"{answer} is not an option")

    def save_to_db(self, question, answer):
        new_row = FlashCard(question=question, answer=answer, box_number=1)
        self.session.add(new_row)
        self.session.commit()

    def practice_flashcards(self):
        flashcards = self.query_db()
        if len(flashcards) == 0:
            print("There is no flashcard to practice!")
        for flashcard in flashcards:
            print(f"Question: {flashcard.question}")
            print('press "y" to see the answer:')
            print('press "n" to skip:')
            print('press "u" to update:')
            answer = input()
            print()
            if answer == "y":
                print(f"Answer: {flashcard.answer}")
                self.learning_menu(flashcard)
            elif answer == "n":
                self.learning_menu(flashcard)
            elif answer == "u":
                self.update_menu(flashcard)

    def learning_menu(self, flashcard):
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        answer = input()
        print()

        if answer == "y":
            if flashcard.box_number == 3:
                self.session.delete(flashcard)
            else:
                flashcard.box_number += 1
        elif answer == "n":
            if flashcard.box_number == 1:
                pass
            else:
                flashcard.box_number -= 1

        self.session.commit()

    def query_db(self):
        return self.session.query(FlashCard).all()

    def update_menu(self, flashcard):
        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')
        answer = input()

        if answer == "e":
            self.update_flashcard(flashcard)
        elif answer == "d":
            self.delete_flashcard(flashcard)
        else:
            return

    def update_flashcard(self, flashcard):
        print(f"current question: {flashcard.question}")
        flashcard.question = input("please write a new question:\n")
        print(f"current answer: {flashcard.answer}")
        flashcard.answer = input("please write a new answer:\n")
        print()
        self.session.commit()

    def delete_flashcard(self, flashcard):
        self.session.delete(flashcard)
        self.session.commit()
        print()


_ = MemorizationTool()
