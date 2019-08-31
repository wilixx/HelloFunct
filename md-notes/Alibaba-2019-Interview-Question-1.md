# 阿里巴巴2019年软件开发笔试题总结 #

> **问题一、圆圈中最幸福男生位置、给定女生个数滑动窗包含的最多男生数量**
> 
> 直接上代码：
   
    
    package archive;
	import java.io.*;
	import java.util.*;
	import java.text.*;
	import java.math.*;
	import java.util.regex.*;
	import javafx.util.Pair;
	public class Main {
	/** 请完成下面这个函数，实现题目要求的功能 **/
	    /** 当然，你也可以不按照这个模板来作答，完全按照自己的想法来 ^-^  **/
	    static String getIndexAndLongest(String users,Integer k) {
	
	        String Index = null;
	        String Longest = null;
	        String result = "";
	        Index = getIndex(users);
	        Longest = getLongest(users,k);
	        // result = Integer.toString(Index )+ Integer.toString(Longest);
	        result = Index + " " + Longest;
	        return result;
	    }
	
	    static String getIndex(String users) {
	        String result = "";
	        List<Integer> neighborList = new ArrayList<Integer>();
	        if(users.isEmpty()){return result;}
	        int tempCounter = 0;
	        int posIndex = 0;
	        for(char i :users.toCharArray()){
	            if(i == 'g'){tempCounter ++;}
	            if(i == 'b'){
	                neighborList.add(tempCounter);
	                tempCounter = 0;
	                neighborList.add(users.length()*2);
	            }
	            posIndex++;
	        }
	        neighborList.add(tempCounter); //放入最末尾一个数；
	        //for(Object x:neighborList){System.out.println(x);}
	        int leftNum = 0;
	        int rightNum =0;
	        int positionAcc = 0;
	        HashMap<Integer,Integer> tempMap = new HashMap<Integer,Integer>();
	        for(int a=1;a <= (neighborList.size()-2);a=a+2){
	            positionAcc = positionAcc + neighborList.get(a-1)+1;
	            if(a == 1){
	                leftNum = neighborList.get(0)+neighborList.get(neighborList.size()-1);
	                rightNum = neighborList.get(a+1);
	            }
	            else if( a == neighborList.size()-2 ){
	                leftNum = neighborList.get(a-1);
	                rightNum = neighborList.get(a+1) + neighborList.get(0);
	            }
	            else {
	                leftNum = neighborList.get(a-1);
	                rightNum = neighborList.get(a+1);
	            }
	            tempMap.put(positionAcc-1,leftNum+rightNum);
	        }
	        Integer maxValue = 0;
	        Integer maxPos = 0;
	        for(Integer key:tempMap.keySet()){
	            //System.out.println("Boy position is : "+key+";"+"Girls count: "+tempMap.get(key));
	            if(tempMap.get(key) > maxValue){
	                maxValue = tempMap.get(key);
	                maxPos = key;
	            }
	        }
	        result = Integer.toString(maxPos);
	        return result;
	    }
	    static String getLongest(String users,Integer k) {
	        String result = "";
	        List<Integer> neighborList = new ArrayList<Integer>();
	        if(users.isEmpty()){return result;}
	        int tempCounter = 0;
	        int posIndex = 0;
	        for(char i :users.toCharArray()){
	            if(i == 'b'){tempCounter ++;}
	            if(i == 'g'){
	                neighborList.add(tempCounter);
	                tempCounter = 0;
	                neighborList.add(users.length()*2);
	            }
	            posIndex++;
	        }
	        neighborList.add(tempCounter); //放入最末尾一个数；
	        //for(Object x:neighborList){System.out.println(x);}
	        // 开始计算最大值
	        int positionAcc = 0;//窗口起点女生位置记录
	        HashMap<Integer,Integer> tempMap = new HashMap<Integer,Integer>();
	
	        for(int a=1;a <= (neighborList.size()-2);a=a+2){//定一个anchor
	            positionAcc = positionAcc + neighborList.get(a-1)+1;
	            // 初始化男生数目
	            int sumBoys =0;
	            sumBoys = neighborList.get(a-1);//窗口起点女生位置记录
	            if(a==1){sumBoys = neighborList.get(0)+ neighborList.get(neighborList.size()-1);}
	            //累加男生数目
	            int boysToCatchPositon = 0;
	            for(int windows =1;windows<=k;windows++){
	                boysToCatchPositon = a+(windows*2-1);
	                if(boysToCatchPositon == neighborList.size()-1){
	                    sumBoys += neighborList.get(neighborList.size()-1);
	                    sumBoys += neighborList.get(0);
	                }
	                else if(boysToCatchPositon > neighborList.size()-1){
	                    boysToCatchPositon = boysToCatchPositon - (neighborList.size()-1);
	                    sumBoys += neighborList.get(boysToCatchPositon);
	                }
	                else{sumBoys += neighborList.get(boysToCatchPositon);}
	            }
	            tempMap.put(positionAcc-1,sumBoys);
	        }
	        Integer maxValue = 0;
	        Integer maxPos = 0;
	        for(Integer key:tempMap.keySet()){
	            // System.out.println("Girl anchor position is : "+key+";"+"Boys count: "+tempMap.get(key));
	            if(tempMap.get(key) > maxValue){
	                maxValue = tempMap.get(key);
	                maxPos = key;//不进行返回
	            }
	        }
	        result = Integer.toString(maxValue);
	        return result;
	    }
	    public static void main(String[] args){
	        Scanner in = new Scanner(System.in);
	        String res;
	        String _users;
	        Integer _k;
	        try {
	            _users = in.nextLine();
	            _k = in.nextInt();
	        } catch (Exception e) {
	            _users = null;
	            _k = 1;
	        }
	        res = getIndexAndLongest(_users,_k);
	        System.out.println("Final result is : "+res);
	    }
	}

