import time
import __builtin__

class timerbank:
    def __init__(self,name='root'):
        clock_overheads = []
        for i in range(1000):
            o_clock = time.clock()
            o_clock = time.clock() - o_clock
            clock_overheads.append(o_clock)
        self.__o_clock = sum(clock_overheads)/float(len(clock_overheads))
        self.__o_begin = time.clock()
        self.name = name
        self.begin = None
        self.end = None
        self.total_time = 0
        self.state = 2 # 0 is start, 1 is pause, 2 is stop
        self.subtimers = dict()
        self.subruntimes = dict()
        self.overhead = time.clock() - self.__o_begin + 2*self.__o_clock
        if name=='root':
            __builtin__.tb = self
    
    def __getitem__(self,tname):
        self.__o_begin = time.clock()
        if tname not in self.subtimers.keys():
            self._add(tname)
            #raise IndexError("No such subtimer " + str(tname))
        self.overhead += time.clock() - self.__o_begin + 2*self.__o_clock
        return self.subtimers[tname]
    
    def _add(self,tname):
        self.__o_begin = time.clock()
        self.subtimers[tname] = timerbank(tname)
        self.subruntimes[tname] = 0
        self.overhead += time.clock() - self.__o_begin + 2*self.__o_clock
        return self.subtimers[tname]
    
    def names(self):
        return self.subtimers.keys()
    
    def _remove(self,tname):
        self.__o_begin = time.clock()
        del self[tname]
        del self.subruntimes[tname]
        self.overhead += time.clock() - self.__o_begin + 2*self.__o_clock
    
    def start(self,tname=None):
        self.__o_begin = time.clock()
        if tname == None:
            if self.state != 0:
                self.state = 0
                self.overhead += time.clock() - self.__o_begin + 2*self.__o_clock
                self.begin = time.clock()
        else:
            if tname not in self.names():
                self._add(tname)
            self.overhead += time.clock() - self.__o_begin + 2*self.__o_clock
            self[tname].start()
    
    def pause(self,tname=None):
        p = time.clock()
        self.__o_begin = time.clock()
        if tname == None:
            if self.state == 0:
                self.total_time += p-self.begin
                self.begin = None
            self.state = 1
            self.overhead += time.clock() - self.__o_begin + 3*self.__o_clock
        else:
            if tname not in self.names():
                raise IndexError("No such subtimer " + tname)
            self.overhead += time.clock() - self.__o_begin + 3*self.__o_clock
            self[tname].pause()
    
    def stop(self,tname=None):
        e = time.clock()
        self.__o_begin = time.clock()
        if tname == None:
            if self.state == 0:
                self.total_time += e-self.begin
            self.state = 2
            self.begin = None
            self.end = None
            self.overhead += time.clock() - self.__o_begin + 3*self.__o_clock
            return self.total_time
        else:
            if tname not in self.names():
                raise IndexError("No such subtimer " + str(tname))
            self.overhead += time.clock() - self.__o_begin + 3*self.__o_clock
            return self[tname].stop()
    
    def runtime(self):
        return self.total_time
    
    def reset(self):
        self.__init__()
    
    def stop_all(self):
        self.stop()
        for s in self.subtimers.values():
            s.stop_all()
    
    def pause_all(self):
        self.pause()
        for s in self.subtimers.values():
            s.pause_all()
    
    def total_overhead(self):
        suboverhead = 0
        for s in self.subtimers.values():
            suboverhead += s.total_overhead()
        return self.overhead + suboverhead
    
    def show(self,overhead=False,prepend=''):
        if overhead:
            if self.name == 'root':
                o = " (total: " + "%.4f" % self.total_overhead() + ")"
            else:
                o = " (" + "%.4f" % self.overhead + ")"
        else:
            o = ''
        print prepend+self.name+": " + "%.4f" % self.runtime() + o
        for n in self.names():
            self.subtimers[n].show(overhead=overhead, prepend=prepend+'---')

timerbank()