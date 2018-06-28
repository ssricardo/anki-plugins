from exception import InvalidConfiguration
import const

class Prioritizer:

    multiplier = {
        const.Priority.LOW: float(150),
        const.Priority.HIGH: float(75)
    }

    @classmethod
    def setMultiplier(clz, key, value): 
        import math

        if math.isnan(value):
            raise InvalidConfiguration('Value should be a number. Got: {}'.format(value))

        if key == const.Priority.HIGH and value >= 100:
            raise InvalidConfiguration('''The multiplier index should be higher than 1 for priorities above normal. 
                Got {}. Check the addon configuration. '''.format(value))
        elif key == const.Priority.LOW and value <= 100:
            raise InvalidConfiguration('''The multiplier index should be lower than 1 for priorities below normal. 
            Got {}. Check the addon configuration. '''.format(value))
        
        clz.multiplier[key] = float(value)

    @classmethod
    def setPriority(clz, note, level):
        if not note or note == None:
            print('Card Null')
            showWarning('Could not get the instance of note. Cancelling process...')
            return

        if level == const.Priority.LOW:
            note.delTag(const.Tag.HIGH)
            note.addTag(const.Tag.LOW)
            priorityStr = 'low'
        elif level == const.Priority.HIGH:
            note.delTag(const.Tag.LOW)
            note.addTag(const.Tag.HIGH)
            priorityStr = 'high'
        else:
            note.delTag(const.Tag.LOW)
            note.delTag(const.Tag.HIGH)
            priorityStr = 'normal'

        note.flush()
        tooltip('Priority set as {}'.format(priorityStr))

    @classmethod
    def getPrioritizedTime(clz, card, resTime):
        """
            Get the estimated time to be shown on top of buttons
        """

        note = card._note

        if note.hasTag(const.Tag.HIGH):
            resTime = int(resTime * (clz.multiplier[const.Priority.HIGH] / 100))
        if note.hasTag(const.Tag.LOW):
            resTime = int(resTime * (clz.multiplier[const.Priority.LOW] / 100))

        return resTime


    @staticmethod
    def getNextInterval(scheduleInstance, *args, **kargs):
        """ Decorator for estimate next schedule time for a given option. 
            This time is shown above the card while studying
        """

        f = kargs['_old']
        res = f(scheduleInstance, args[0], args[1])
        card = args[0]  # card

        return Prioritizer.getPrioritizedTime(card, res)

    @staticmethod
    def priorityUpdateRevision(scheduleInst, *args, **kargs):
        """ Decorator for get next revision date, based on priority. 
            Used to schedule the next date.
        """

        f = kargs['_old']
        card = args[0]
        f(scheduleInst, card, args[1])     # _updateRevIvl(self, card, ease)
        card.ivl = Prioritizer.getPrioritizedTime(card, card.ivl)

# =========================== exec ================================

# ------------------------ Interface with anki --------------------
def init():
    Scheduler.nextIvl = wrap(Scheduler.nextIvl, Prioritizer.getNextInterval, 'around')
    Scheduler._updateRevIvl = wrap(Scheduler._updateRevIvl, Prioritizer.priorityUpdateRevision, 'around')

    print(Prioritizer.multiplier)

# ------------------------ External runnable ----------------------
if __name__ == '__main__':
    # self contained tests

    import unittest

    class TNote:
        _tag = None

        def hasTag(self, str):
            return str == self._tag

    class TCard:

        _note = TNote()

    class Tester(unittest.TestCase):

        def test_highTime(self):
            c = TCard()
            c._note._tag = const.Tag.HIGH
            
            time = Prioritizer.getPrioritizedTime(c, 1000)
            self.assertEqual(750, time)

        def test_lowTime(self):
            c = TCard()
            c._note._tag = const.Tag.LOW
            
            time = Prioritizer.getPrioritizedTime(c, 1000)
            self.assertEqual(1500, time)


    unittest.main()
else:
    from anki.hooks import addHook, wrap
    from anki.sched import Scheduler
    from aqt.utils import showWarning, tooltip